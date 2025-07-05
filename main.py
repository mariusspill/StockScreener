import yfinance as yf
import pandas as pd
import tickers
import data as dt
import os
import json
import alphavantagapi as ava


pd.set_option('display.max_rows', None)  # Show all rows

def get_net_income_yfinance(ticker: str, year: int):
    year = str(year)

    data = yf.Ticker(ticker)

    try:
        result = data.financials.loc["Net Income"][year].values[0]
    except:
        result = "no data"

        
    return result

print(ava.get_income_statement_alphavantage("A"))