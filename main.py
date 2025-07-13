import yfinance as yf
import pandas as pd
import tickers
import alphavantagedata as dt
import os
import json
import alphavantagapi as ava
import analysis_key_numbers as a
import analysis_screening as ascreen
import dcf
import dbdata

pd.set_option('display.max_rows', None)  # Show all rows

tckrs = tickers.getTickers("./list.txt")

ascreen.print_analysis(tckrs)