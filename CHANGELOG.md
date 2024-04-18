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
