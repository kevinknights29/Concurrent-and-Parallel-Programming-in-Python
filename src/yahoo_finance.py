from __future__ import annotations

import random
import time
from collections import namedtuple
from multiprocessing import Queue
from threading import Thread

from lxml import html
from requests import get  # type: ignore

Stock = namedtuple("Stock", ["ticker", "price", "price_change", "percentual_change"])


class YahooFinancePriceScheduler(Thread):
    """A thread class for scheduling Yahoo Finance price retrieval tasks.

    Args:
        Thread: The base class for creating threads.
    """

    STOP_SIGNAL = "STOP"

    def __init__(
        self,
        queue: Queue,
        **kwargs,
    ) -> None:
        """Initializes a YahooFinancePriceScheduler instance.

        Args:
            queue (Queue): The queue to retrieve stock tickers.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(**kwargs)
        self._queue = queue
        self.start()

    def run(self) -> None:
        """Runs the thread to retrieve stock price information.

        This method continuously retrieves stock tickers from the queue,
        fetches price information for each ticker, and prints the results.

        """
        while True:
            ticker = self._queue.get()
            if ticker == self.STOP_SIGNAL:
                break
            price_info = YahooFinancePriceWorker(ticker).get_price_information()
            print(
                (
                    f"Stock: {price_info.ticker}, "
                    f"Price: {price_info.price}, "
                    f"Change: {price_info.price_change}, "
                    f"Percentual Change: {price_info.percentual_change}"
                ),
            )
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
        print(f"Getting price for {self._ticker}")
        response = get(self._url)
        if response.status_code == 200:
            page_content = response.text
            price = (
                html.fromstring(page_content)
                .xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div[1]/fin-streamer[1]')[0]
                .text
            )
            price_change = (
                html.fromstring(page_content)
                .xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div[1]/fin-streamer[2]/span')[0]
                .text
            )
            percentual_change = (
                html.fromstring(page_content)
                .xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div[1]/fin-streamer[3]/span')[0]
                .text
            )
            return Stock(self._ticker, price, price_change, percentual_change)
        else:
            raise Exception(f"Failed to fetch price for {self._ticker}")
