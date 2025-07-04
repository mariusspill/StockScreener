import yfinance as yf
import pandas as pd
import tickers
import data as dt


pd.set_option('display.max_rows', None)  # Show all rows


tckrs = tickers.getTickers()

data = yf.Ticker("MSFT")

def get_net_income(ticker: str, year: int):
    year = str(year)

    data = yf.Ticker(ticker)

    try:
        result = data.financials.loc["Net Income"][year].values[0]
    except:
        result = "no data"

        
    return result


for ticker in tckrs:
    for year in range(2024, 2020, -1):
        print(ticker, ",", year, ": ", get_net_income(ticker, year))
