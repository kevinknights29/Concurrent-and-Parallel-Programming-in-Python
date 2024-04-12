from __future__ import annotations

from threading import Thread

from lxml import html
from requests import get  # type: ignore


class YahooFinancePriceWorker(Thread):
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

    def __init__(self, ticker, **kwargs):
        """Initializes the worker with the given stock ticker and starts it.

        Args:
            ticker (str): The stock ticker to fetch the price for.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(**kwargs)
        self._ticker = ticker
        self._url = self.BASE_URL + self._ticker
        self.start()

    def run(self) -> None:
        """Fetches and prints the price of the stock ticker.

        This method is automatically called when the thread is started.
        It fetches the price of the stock ticker from Yahoo Finance and prints it.
        If the fetch fails, it prints an error message.
        """
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
                .xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div[1]/fin-streamer[3]/span')[1]
                .text
            )
            print(
                (
                    f"Report for {self._ticker}: "
                    f"Price {price}, "
                    f"Change {price_change}, "
                    f"Percentual Change {percentual_change}"
                ),
            )
        else:
            print(f"Failed to get price for {self._ticker}")
