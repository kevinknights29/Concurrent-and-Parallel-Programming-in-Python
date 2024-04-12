from __future__ import annotations

import time

from src import wikipedia
from src import yahoo_finance


def main():
    start_time = time.time()

    wiki_worker = wikipedia.WikiWorker()
    current_workers = []
    for company_ticker in wiki_worker.get_page_content():
        ticker = company_ticker[0]
        yahoo_worker = yahoo_finance.YahooFinancePriceWorker(ticker)
        current_workers.append(yahoo_worker)

    for worker in current_workers:
        worker.join()

    print(f"Time taken: {time.time() - start_time:.2f} seconds")


if __name__ == "__main__":
    main()
