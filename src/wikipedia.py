from __future__ import annotations

from typing import Generator

import requests  # type: ignore
from bs4 import BeautifulSoup


class WikiWorker:
    """
    A class used to scrape data from a specific Wikipedia page.

    Attributes:
        _url (str): The URL of the Wikipedia page to be scraped.
        _page (str): The HTML content of the page.
    """

    def __init__(self):
        """
        Constructs the necessary attributes for the WikiWorker object.
        """
        self._url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        self._page = None

    def _extract_company_symbols(self) -> Generator[list[str], None, None]:
        """
        Extracts the company symbols from the Wikipedia page.

        The method uses BeautifulSoup to parse the HTML of the page and extract the company symbols
        from a table with the id "constituents". It yields each company symbol one by one.

        Yields:
            Generator[list[str], None, None]: A generator that yields each company symbol.
        """
        soup = BeautifulSoup(self._page, "html.parser")
        table = soup.find("table", {"id": "constituents"})
        rows = table.find_all("tr")[1:]
        for row in rows:
            symbol = row.find_all("td")[0].text.strip("\n")
            yield [symbol]

    def get_page_content(self) -> Generator[list[str], None, None]:
        """
        Fetches the page content if it hasn't been fetched already, and yields the company symbols.

        The method first checks if the page content has already been fetched.
        If not, it sends a GET request to the URL and stores the response text in `self._page`.
        If the status code of the response is not 200, it prints an error message and returns an empty list.
        Otherwise, it calls the `_extract_company_symbols` method with the response text and yields the company symbols.

        Returns:
            Generator[list[str], None, None]: A generator that yields the company symbols if the page content
            was fetched successfully, or an empty list otherwise.
        """
        if not self._page:
            response = requests.get(self._url)
            if response.status_code != 200:
                print("Failed to fetch page content")
                yield []

        self._page = response.text

        yield from self._extract_company_symbols()
