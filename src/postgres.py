from __future__ import annotations

import logging
import os
from multiprocessing import Queue
from threading import Thread

from dotenv import find_dotenv
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy import URL
from sqlalchemy.sql.elements import TextClause

# Initialize the logger
logger = logging.getLogger(__name__)

# Load the environment variables
_ = load_dotenv(find_dotenv())
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")


class PostgresScheduler(Thread):
    """A class used to schedule tasks for Postgres database operations.

    Attributes:
        STOP_SIGNAL (str): A constant that represents the signal to stop the thread.
    """

    STOP_SIGNAL = "STOP"

    def __init__(self, input_queue: Queue, **kwargs) -> None:
        """Initializes the PostgresScheduler with a queue of tasks.

        Args:
            queue (Queue): The queue of tasks to be executed.
            **kwargs (dict): Arbitrary keyword arguments.
        """
        super().__init__(**kwargs)
        self._input_queue = input_queue
        self.start()

    def run(self) -> None:
        """Continuously gets tasks from the queue and executes them until the STOP_SIGNAL is received."""
        while True:
            data = self._input_queue.get()
            if data == self.STOP_SIGNAL:
                break
            PostgresWorker(data).insert_data()


class PostgresWorker:
    """Handles the insertion of data into a Postgres database.

    Attributes:
        CONNECTION_STRING (URL): The connection string for the Postgres database.
    """

    CONNECTION_STRING = URL.create(
        drivername="postgresql+psycopg",
        username=DB_USERNAME,
        password=DB_PASSWORD,
        database=DB_NAME,
        host=DB_HOST,
        port=DB_PORT,
    )

    def __init__(self, data: dict) -> None:
        """Initializes the PostgresWorker with the data to be inserted.

        Args:
            data (dict): The data to be inserted.
                It should contain the keys 'ticker', 'price', 'price_change', and 'percentual_change'.
        """
        self._data = data
        self._ticker = self._data["ticker"]
        self._price = self._data["price"].replace(",", "")
        self._price_change = self._data["price_change"]
        self._percentual_change = self._data["percentual_change"]

    def _create_insert_query(self) -> TextClause:
        """Creates the SQL query for inserting data into the 'prices' table.

        Returns:
            TextClause: The SQL query as a TextClause object.
        """
        query = text(
            "INSERT INTO prices (ticker, price, price_change, percentual_change)"
            "VALUES (:ticker, :price, :price_change, :percentual_change);",
        )
        return query

    def insert_data(self) -> None:
        """Executes the SQL query to insert data into the 'stocks' table."""
        engine = create_engine(self.CONNECTION_STRING)
        with engine.connect() as conn:
            conn.execute(
                self._create_insert_query(),
                {
                    "ticker": self._ticker,
                    "price": self._price,
                    "price_change": self._price_change,
                    "percentual_change": self._percentual_change,
                },
            )
            conn.commit()
            logger.info("Query executed successfully.")
