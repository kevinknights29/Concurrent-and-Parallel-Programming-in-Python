from __future__ import annotations

import logging.config
import time
from pathlib import Path

from src.pipeline import executor
from src.utils import config

CONFIG = config.config()
PIPELINE_CONFIG = CONFIG["pipeline"]

# Initialize the logger
logger = logging.getLogger(__name__)


def _setup_logging() -> None:
    """Configures the logging module using the configuration in config.json."""

    Path("logs").mkdir(parents=True, exist_ok=True)
    Path("logs/app.log").touch(exist_ok=True)  # filename should match the one in config.json
    Path("logs/errors.log").touch(exist_ok=True)  # filename should match the one in config.json

    # Configure ROOT logger
    logging.config.dictConfig(CONFIG["logging"])


def main() -> None:
    """Runs the main function to fetch stock price information using Yahoo Finance.

    This function initializes a queue for stock tickers, creates YahooFinancePriceScheduler
    instances to fetch price information concurrently, retrieves stock tickers from
    Wikipedia using WikiWorker, puts the tickers into the queue, signals the schedulers
    to stop after processing all tickers, and finally waits for all schedulers to finish.

    """
    _setup_logging()

    logger.debug("Starting pipeline.")
    start_time = time.time()

    pipeline = executor.PipelineExecutor(pipeline_config=CONFIG["pipeline"])
    pipeline.setup_pipeline()

    pipeline._workers["wiki"].get_page_content()

    for _ in pipeline._schedulers["yahoo"]:
        pipeline._queues["tickers"].put(PIPELINE_CONFIG["stop_signal"])

    logger.debug(f"Time taken: {time.time() - start_time:.2f} seconds")


if __name__ == "__main__":
    main()
