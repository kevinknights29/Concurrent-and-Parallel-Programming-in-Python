from __future__ import annotations

import json
import logging.config
import time
from multiprocessing import Queue
from pathlib import Path

from src import postgres
from src import wikipedia
from src import yahoo_finance

# Define the number of scheduler instances
YAHOO_SCHEDULERS = 5
POSTGRES_SCHEDULERS = 5

# Initialize the logger
logger = logging.getLogger(__name__)


def _setup_logging() -> None:
    """Configures the logging module using the configuration in config.json."""

    Path("logs").mkdir(parents=True, exist_ok=True)
    Path("logs/app.log").touch(exist_ok=True)  # filename should match the one in config.json
    Path("logs/errors.log").touch(exist_ok=True)  # filename should match the one in config.json

    # Configure ROOT logger
    LOGGING_CONFIG = json.load(open("config.json"))["logging"]
    logging.config.dictConfig(LOGGING_CONFIG)


def main() -> None:
    """Runs the main function to fetch stock price information using Yahoo Finance.

    This function initializes a queue for stock tickers, creates YahooFinancePriceScheduler
    instances to fetch price information concurrently, retrieves stock tickers from
    Wikipedia using WikiWorker, puts the tickers into the queue, signals the schedulers
    to stop after processing all tickers, and finally waits for all schedulers to finish.

    """
    _setup_logging()

    start_time = time.time()
    tickers_queue: Queue = Queue()
    postgres_queue: Queue = Queue()

    wiki_worker = wikipedia.WikiWorker()
    yahoo_schedulers = []
    postgres_schedulers = []

    for _ in range(YAHOO_SCHEDULERS):
        yahoo_scheduler = yahoo_finance.YahooFinancePriceScheduler(
            input_queue=tickers_queue,
            output_queue=postgres_queue,
        )
        yahoo_schedulers.append(yahoo_scheduler)

    for _ in range(POSTGRES_SCHEDULERS):
        postgres_scheduler = postgres.PostgresScheduler(postgres_queue)
        postgres_schedulers.append(postgres_scheduler)

    for company_ticker in wiki_worker.get_page_content():
        ticker = company_ticker[0]
        tickers_queue.put(ticker)

    for _ in range(YAHOO_SCHEDULERS):
        tickers_queue.put(yahoo_finance.YahooFinancePriceScheduler.STOP_SIGNAL)

    for scheduler in yahoo_schedulers:
        scheduler.join()

    logger.debug(f"Time taken: {time.time() - start_time:.2f} seconds")


if __name__ == "__main__":
    main()
