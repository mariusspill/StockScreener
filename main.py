import yfinance as yf
import pandas as pd
import tickers
import data as dt
import os
import json
import alphavantagapi as ava
import analysis as a
import dcf

pd.set_option('display.max_rows', None)  # Show all rows

def get_net_income_yfinance(ticker: str, year: int):
    year = str(year)

    data = yf.Ticker(ticker)

    try:
        result = data.financials.loc["Net Income"][year].values[0]
    except:
        result = "no data"

        
    return result


def get_marketCap():
    data = yf.Ticker("A")
    return data.info['marketCap']

def get_PE():
    data = yf.Ticker("A")
    print(data.info)

tckrs = tickers.getTickers("./list.txt")


def print_analysis(ticker: str):
    print()
    print(ticker)
    print(a.average_net_income_5years(ticker))
    print(a.variance_net_income_5years(ticker))
    print(a.standard_deviation_net_income_5years(ticker))
    print(a.coefficient_of_variation_net_income_5years(ticker))


# for ticker in tckrs:
#     print_analysis(ticker)

def fetch_data():
    tckrs = tickers.getTickers("./Data/Indices/s&p500.txt")

    i = 0

    for ticker in tckrs:
        cf = ava.get_balance_sheet_alphavantage(ticker)
        print(cf)
        ava.save_json_raw(ticker, cf, "balanceSheet")
        i += 1

        if i > 3:
            return


fetch_data()