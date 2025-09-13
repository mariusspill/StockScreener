# StockScreener
python based stock screener for value investing

# Disclaimer
This is a first prototype! Nothing of it is either polished nor production ready. It is supposed to showcase technologies I experimented with and which I want to develop further in an environment that I am pashioned about. Components might be missing and the database is currently offline since it is run on my home pc in Germany.

# Components
* Webinterface: Hosted by Flask and created in raw HTML, CSS and JS. Includes a filter and display of results that meet filtered conditions
* Database: Self-Hosted MySQL Database that stores high quality finance data like company infos and annual income statements or balance sheets
  - Included API pipeline from both YahooFinance and AlphaAdvantage for high quality data
  - Some handchecked data from official 10-K and SEC sources
* Valuation Models:
  - Automated Discounted Cashflow Model
  - First ML Models (mostly linear regression models)
* Screening logic: loads data from the database and applies a python script to detect stocks that meet certain conditions
