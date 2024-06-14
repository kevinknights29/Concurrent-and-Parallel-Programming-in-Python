from __future__ import annotations

import importlib
import logging
from multiprocessing import Queue
from typing import Any

# Initialize the logger
logger = logging.getLogger(__name__)


class PipelineExecutor:
    def __init__(self, pipeline_config: dict) -> None:
        self._pipeline_config = pipeline_config
        self._queues: dict[str, Queue] = {}
        self._workers: dict[str, Any] = {}
        self._schedulers: dict[str, Any] = {}

    def _initialize_queues(self):
        logger.debug("Initializing Queues.")
        for item in self._pipeline_config["queues"]:
            name = item["name"]
            description = item["description"]
            self._queues[name] = Queue
            logger.info("Initialized Queue: %s, with Description: %s", name, description)

    def _initialize_workers(self):
        logger.debug("Initializing Workers.")
        for item in self._pipeline_config["workers"]:
            name = item["name"]
            description = item["description"]
            _class = getattr(importlib.import_module(item["location"]), item["class"])
            input_queue = item.get("input_queue")
            output_queue = item.get("output_queue")
            init_params = {
                "input_queue": self._queues.get(input_queue),
                "output_queue": self._queues.get(output_queue),
            }
            self._workers[name] = _class(**init_params)
            logger.info("Initialized Worker: %s using Class %s, with Description: %s", name, _class, description)

    def _initialize_schedulers(self):
        logger.debug("Initializing Schedulers.")
        for item in self._pipeline_config["schedulers"]:
            name = item["name"]
            description = item["description"]
            instances = item["instances"]
            _class = getattr(importlib.import_module(item["location"]), item["class"])
            input_queue = item.get("input_queue")
            output_queue = item.get("output_queue")
            init_params = {
                "input_queue": self._queues.get(input_queue),
                "output_queue": self._queues.get(output_queue),
            }
            self._schedulers[name] = [_class(**init_params) * instances]
            logger.info(
                "Initialized %s Schedulers: %s using Class %s, with Description: %s",
                instances,
                name,
                _class,
                description,
            )

    def _join_schedulers(self):
        logger.debug("Joining Schedulers.")
        to_join = []
        for _, schedulers in self._schedulers.items():
            to_join += schedulers
        for scheduler in to_join:
            scheduler.join()
        logger.info("%s Schedulers joined.", len(self._schedulers))

    def setup_pipeline(self):
        self._initialize_queues()
        self._initialize_workers()
        self._initialize_schedulers()
