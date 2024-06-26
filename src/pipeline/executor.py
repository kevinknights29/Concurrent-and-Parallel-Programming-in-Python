from __future__ import annotations

import importlib
import logging
from multiprocessing import Queue
from typing import Any

# Initialize the logger
logger = logging.getLogger(__name__)


class PipelineExecutor:
    """Executes a data processing pipeline based on the provided configuration.

    Attributes:
        _pipeline_config (dict): Configuration for the pipeline.
        _queues (dict[str, Queue]): Dictionary of queues used in the pipeline.
        _workers (dict[str, Any]): Dictionary of worker instances.
        _schedulers (dict[str, Any]): Dictionary of scheduler instances.
    """

    def __init__(self, pipeline_config: dict) -> None:
        """Initializes the PipelineExecutor with the given configuration.

        Args:
            pipeline_config (dict): Configuration for the pipeline.
        """
        self._pipeline_config = pipeline_config
        self._queues: dict[str, Queue] = {}
        self._workers: dict[str, Any] = {}
        self._schedulers: dict[str, Any] = {}

    def _initialize_queues(self) -> None:
        """Initializes the queues as defined in the pipeline configuration."""
        logger.debug("Initializing Queues.")
        for key, values in self._pipeline_config["queues"].items():
            description = values["description"]
            self._queues[key] = Queue()
            logger.info("Initialized Queue: %s, with Description: %s", key, description)

    def _initialize_workers(self) -> None:
        """Initializes the workers as defined in the pipeline configuration."""
        logger.debug("Initializing Workers.")
        for key, values in self._pipeline_config["workers"].items():
            description = values["description"]
            _class = getattr(importlib.import_module(values["module"]), values["class"])
            input_queue = values.get("input_queue")
            output_queue = values.get("output_queue")
            init_params = {
                "input_queue": self._queues.get(input_queue),
                "output_queue": self._queues.get(output_queue),
            }
            self._workers[key] = _class(**init_params)
            logger.info("Initialized Worker: %s using Class %s, with Description: %s", key, _class, description)

    def _initialize_schedulers(self) -> None:
        """Initializes the schedulers as defined in the pipeline configuration."""
        logger.debug("Initializing Schedulers.")
        for key, values in self._pipeline_config["schedulers"].items():
            description = values["description"]
            instances = values["instances"]
            _class = getattr(importlib.import_module(values["module"]), values["class"])
            input_queue = values.get("input_queue")
            output_queue = values.get("output_queue")
            init_params = {
                "input_queue": self._queues.get(input_queue),
                "output_queue": self._queues.get(output_queue),
            }
            self._schedulers[key] = [_class(**init_params) for _ in range(instances)]
            logger.info(
                "Initialized %s Schedulers: %s using Class %s, with Description: %s",
                instances,
                key,
                _class,
                description,
            )

    def _join_schedulers(self) -> None:
        """Joins all the scheduler instances."""
        logger.debug("Joining Schedulers.")
        to_join = []
        for _, schedulers in self._schedulers.items():
            to_join += schedulers
        for scheduler in to_join:
            scheduler.join()
        logger.info("%s Schedulers joined.", len(self._schedulers))

    def setup_pipeline(self) -> None:
        """Sets up the pipeline by initializing queues, workers, and schedulers."""
        self._initialize_queues()
        self._initialize_workers()
        self._initialize_schedulers()
