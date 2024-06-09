## 0.4.0 (2024-06-09)

### Feat

- added mermaid as an extension
- added try except statements around html parsing to log errors related to xpaths
- added xpath parsing from config
- added utils submodule
- added web scrapping xpath to config
- added errors.log creation to setup_logging func
- added error_file to log config for errors.log file creation
- added .dockerignore for python
- added PostgresScheduler and postgress queue processing
- added output_queue to YahooFinancePriceScheduler
- added PostgresScheduler and PostgresWokrer classes
- added table schema
- added postgres image with init scripts
- added network so services can access one another
- added docker compose to spin up app and postgres services
- added docker image for app

### Fix

- formatted price string to remove commas
- updated table name to prices
- replaced DB_HOST env var with service name db
- updated DB_HOST ip
- removed context manager from engine
- updated driver to psycopg3
- added deps to make psycopg2 work
- updated argument passed to create_engine
- deserialized namedtuple to dict
- updated retrieval of only one element out of xpath
- added copy of logging config
- updated prod dependencies
- added env vars for python app
- added user postgres
- added PG_USER env var
- updated rule to ignore all pycache files
- copying src package as a directory
- added src package and main.py to container
- added user to healthcheck
- removed trailing comma
- updated quotes to avoid unrecognized chars
- removed version property, is obsolete

### Refactor

- updated installation of psycopg3
- updated logging config parsing
- updated exclusion rules for logs
- added key for logging config
- removed Github Copilot extensions
- updated precommit hooks version
- updated pre-commit hooks version
- added python-dotenv as dep
- added sqlalchemy and psycopg2 as deps
- added postgres image build due to custom init scripts
- updated pre-commit hooks
- updated pre-commit hooks version

## 0.3.0 (2024-04-19)

### Feat

- added config json file
- added logging to app
- added logging to submodules

### Refactor

- updated pre-commit hooks version

## 0.2.0 (2024-04-18)

### Feat

- updated main to leverage scheduler
- added YahooFinancePriceScheduler class, Stock namedtuple, and updated YahooFinancePriceWorker inheritance

### Refactor

- removed print in YahooFinancePriceWorker get_price_information func

## 0.1.0 (2024-04-12)

### Feat

- added main script to extract information in parallel
- added submodule yahoo_finance with class YahooFinancePriceWorker
- added lxml as a dependency
- added test to check proper functionality
- added dependencies
- added wikipedia submodule with WikiWorker class
- added requests and bs4 as deps

### Refactor

- added random sleep to delay execution
- updated pre-commit hooks version
- updated requirements.txt with new dependencies
- replaced symbol with ticker for better comprehension
- added types-requests for mypy

## 0.0.1 (2024-04-11)

### Refactor

- updated version to 0.0.1

## 0.4.1 (2024-04-11)

### Refactor

- updated project name and description
- updated pre-commit hooks
