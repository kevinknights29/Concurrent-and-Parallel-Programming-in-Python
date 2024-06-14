from __future__ import annotations

import json
import logging

from src.utils import constants

# Initialize the logger
logger = logging.getLogger(__name__)

conf: dict = {}


def config() -> dict:
    """
    Loads the config.yaml file and returns a dict stored in config

    Returns:
        dict: configuration dictionary
    """

    global conf
    if not conf:
        logger.debug("Reading from config file.")
        with open(constants.CONFIG_FILE, encoding="utf-8") as file:
            conf = json.load(file)
    logger.info("Config loaded.")
    return conf
