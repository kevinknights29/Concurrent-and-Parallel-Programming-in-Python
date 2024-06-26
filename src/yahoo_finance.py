from __future__ import annotations

import json
import logging
import os
import random
import time
from collections import namedtuple
from multiprocessing import Queue
from threading import Thread

from lxml import html
from requests import get  # type: ignore

from src.utils import constants

# Initialize the logger
logger = logging.getLogger(__name__)

SCRAPPING_CONFIG = json.load(
    open(
        os.path.join(
            constants.ROOT_DIR,
            "config.json",
        ),
    ),
)["finance_yahoo"]

# Define a named tuple to store stock information
Stock = namedtuple("Stock", ["ticker", "price", "price_change", "percentual_change"])


class YahooFinancePriceScheduler(Thread):
    """A thread class for scheduling Yahoo Finance price retrieval tasks.

    Args:
        Thread: The base class for creating threads.
    """

    STOP_SIGNAL = "STOP"

    def __init__(
        self,
        input_queue: Queue,
        output_queue: Queue | None = None,
        **kwargs,
    ) -> None:
        """Initializes a YahooFinancePriceScheduler instance.

        Args:
            input_queue (Queue): The queue to retrieve stock tickers.
            output_queue (Queue): The queue to store information retrieved for further processing.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(**kwargs)
        self._input_queue = input_queue
        self._output_queue = output_queue
        self.start()

    def run(self) -> None:
        """Runs the thread to retrieve stock price information.

        This method continuously retrieves stock tickers from the queue,
        fetches price information for each ticker, and prints the results.

        """
        while True:
            ticker = self._input_queue.get()
            if ticker == self.STOP_SIGNAL:
                if self._output_queue is not None:
                    self._output_queue.put(self.STOP_SIGNAL)
                break
            price_info = YahooFinancePriceWorker(ticker).get_price_information()
            logger.info(
                ("Stock: %s, " "Price: %s, " "Change: %s, " "Percentual Change: %s"),
                price_info.ticker,
                price_info.price,
                price_info.price_change,
                price_info.percentual_change,
            )
            if self._output_queue is not None:
                self._output_queue.put(price_info._asdict())
                logger.info("Ticker %s data has been pushed to an output queue!", ticker)
            time.sleep(random.random())  # Sleep for a random amount of time, max 1 second.


class YahooFinancePriceWorker:
    """A worker thread that fetches and prints the price of a given stock ticker from Yahoo Finance.

    Attributes:
        BASE_URL (str): The base URL for Yahoo Finance stock quotes.
        _ticker (str): The stock ticker to fetch the price for.
        _url (str): The full URL to fetch the price from.

    Args:
        ticker (str): The stock ticker to fetch the price for.
        **kwargs: Arbitrary keyword arguments.
    """

    BASE_URL = "https://finance.yahoo.com/quote/"

    def __init__(self, ticker: str, **kwargs):
        """Initializes the worker with the given stock ticker and starts it.

        Args:
            ticker (str): The stock ticker to fetch the price for.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(**kwargs)
        self._ticker = ticker
        self._url = self.BASE_URL + self._ticker

    def get_price_information(self) -> Stock:
        """Fetches the current price information for the stock.

        This method fetches the current price, price change, and percentual change
        for the given stock ticker from a web source.

        Raises:
            Exception: If there's an issue fetching the price information.

        Returns:
            Stock: A Stock object containing the fetched price information.
        """
        time.sleep(random.random() * 10)  # Sleep for a random amount of time, max 10 seconds.
        response = get(self._url)
        if response.status_code == 200:
            page_content = response.text
            try:
                price = html.fromstring(page_content).xpath(SCRAPPING_CONFIG["price_xpath"])[0].text
            except IndexError:
                logger.error("Something went wrong... Check price's xpath in config.json")
            try:
                price_change = html.fromstring(page_content).xpath(SCRAPPING_CONFIG["price_change_xpath"])[0].text
            except IndexError:
                logger.error("Something went wrong... Check price_change's xpath in config.json")
            try:
                percentual_change = (
                    html.fromstring(page_content).xpath(SCRAPPING_CONFIG["percentual_change_xpath"])[0].text
                )
            except IndexError:
                logger.error("Something went wrong... Check percentual_change's xpath in config.json")

            if len(price_change) > 1:
                price_change = "".join(price_change)
            if len(percentual_change) > 1:
                percentual_change = "".join(percentual_change)

            return Stock(self._ticker, price, price_change, percentual_change)
        else:
            logger.error("Failed to fetch price information for %s", self._ticker)
            raise Exception("Failed to fetch stock price information")
