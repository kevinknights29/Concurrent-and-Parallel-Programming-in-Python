from __future__ import annotations

import logging
from multiprocessing import Queue

import requests  # type: ignore
from bs4 import BeautifulSoup

# Initialize the logger
logger = logging.getLogger(__name__)


class WikiWorker:
    """
    A class used to scrape data from a specific Wikipedia page.

    Attributes:
        _url (str): The URL of the Wikipedia page to be scraped.
        _page (str): The HTML content of the page.
    """

    def __init__(
        self,
        input_queue: Queue | None,
        output_queue: Queue,
        **kwargs,
    ):
        """
        Constructs the necessary attributes for the WikiWorker object.
        """
        self._url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        self._page = None
        self._input_queue = input_queue
        self._output_queue = output_queue

    def _extract_company_ticker(self) -> None:
        """
        Extracts the company ticker from the Wikipedia page.

        The method uses BeautifulSoup to parse the HTML of the page and extract the company tickers
        from a table with the id "constituents". It yields each company ticker one by one.

        Yields:
            Generator[list[str], None, None]: A generator that yields each company ticker.
        """
        soup = BeautifulSoup(self._page, "html.parser")
        table = soup.find("table", {"id": "constituents"})
        rows = table.find_all("tr")[1:]
        for row in rows:
            ticker = row.find_all("td")[0].text.strip("\n")
            self._output_queue.put(ticker)
            logger.info("Ticker %s data has been pushed to an output queue!", ticker)

    def get_page_content(self) -> None:
        """
        Fetches the page content if it hasn't been fetched already, and yields the company tickers.

        The method first checks if the page content has already been fetched.
        If not, it sends a GET request to the URL and stores the response text in `self._page`.
        If the status code of the response is not 200, it prints an error message and returns an empty list.
        Otherwise, it calls the `_extract_company_tickers` method with the response text and yields the company tickers.

        Returns:
            Generator[list[str], None, None]: A generator that yields the company tickers if the page content
            was fetched successfully, or an empty list otherwise.
        """
        if not self._page:
            response = requests.get(self._url)
            if response.status_code != 200:
                logger.error("Failed to fetch page content")
        self._page = response.text
        self._extract_company_ticker()
