# StockScreener
Python based stock screener for value investing.

# Disclaimer
Note: This is an exploratory prototype, developed as a learning project to experiment with full-stack data workflows (data pipelines, ML models, valuation logic, and visualization). It is not production-ready, but serves as a foundation for future development.

# Components
* Webinterface: Hosted by Flask and created in raw HTML, CSS and JS. Includes a filter and display of results that meet filtered conditions
* Database: Self-Hosted MySQL Database that stores high quality finance data like company infos and annual income statements or balance sheets
  - Included API pipeline from both YahooFinance and AlphaAdvantage for high quality data
  - Some handchecked data from official 10-K and SEC sources
* Valuation Models:
  - Automated Discounted Cashflow Model
  - First ML Models (mostly linear regression models)
* Screening logic: loads data from the database and applies a python script to detect stocks that meet certain conditions
