from __future__ import annotations

import time
from multiprocessing import Queue

from src import wikipedia
from src import yahoo_finance

YAHOO_SCHEDULERS = 5


def main() -> None:
    """Runs the main function to fetch stock price information using Yahoo Finance.

    This function initializes a queue for stock tickers, creates YahooFinancePriceScheduler
    instances to fetch price information concurrently, retrieves stock tickers from
    Wikipedia using WikiWorker, puts the tickers into the queue, signals the schedulers
    to stop after processing all tickers, and finally waits for all schedulers to finish.

    """
    start_time = time.time()
    tickers_queue: Queue = Queue()

    wiki_worker = wikipedia.WikiWorker()
    yahoo_schedulers = []

    for _ in range(YAHOO_SCHEDULERS):
        scheduler = yahoo_finance.YahooFinancePriceScheduler(tickers_queue)
        yahoo_schedulers.append(scheduler)

    for company_ticker in wiki_worker.get_page_content():
        ticker = company_ticker[0]
        tickers_queue.put(ticker)

    for _ in range(YAHOO_SCHEDULERS):
        tickers_queue.put(yahoo_finance.YahooFinancePriceScheduler.STOP_SIGNAL)

    for scheduler in yahoo_schedulers:
        scheduler.join()

    print(f"Time taken: {time.time() - start_time:.2f} seconds")


if __name__ == "__main__":
    main()
