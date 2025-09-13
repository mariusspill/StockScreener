# ✅ StockScreener
A Python-based prototype for value investing, exploring full-stack data workflows including data pipelines, machine learning, valuation models, and visualization.

# ⚠️ Disclaimer
Note: This is an exploratory prototype, developed as a learning project to experiment with full-stack data workflows (data pipelines, ML models, valuation logic, and visualization). It is not production-ready, but serves as a foundation for future development.

# 📈 Components
* Web Interface: Flask backend with raw HTML, CSS, and JavaScript frontend. Includes filtering and result display.
* Database: Self-hosted MySQL database storing financial data (company information, annual reports, balance sheets).
  - Integrated pipelines from YahooFinance and AlphaVantage APIs.
  - Augmented with manually validated data from SEC 10-K filings.
* Valuation Models:
  - Automated Discounted Cash Flow (DCF) model.
  - Initial machine learning models (linear regression).
* Screening Logic: Python scripts to load data and apply screening criteria to detect candidate stocks.
