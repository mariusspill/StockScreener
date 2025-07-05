import csv
import os
import json
import pandas as pd

def append_to_financial_data(file: str, ticker: str, year: int, metric: str, value):
    with open(file, mode="a") as file:
        file.write("\n" + ticker + ", " + str(year) + ", " + metric + ", " + str(value))

def append_to_financial_data_by_company(file: str):
    pass

def read_netIncome()-> dict:
    with open("./Data/RawData/ibm/ibm_incomeStatement.json", "r") as file:
        data = json.load(file)
    
    result = dict()

    for i in range(len(data["annualReports"])):
        year = data["annualReports"][i]["fiscalDateEnding"][0:4]
        value = data["annualReports"][i]["netIncome"]
        result[year] = value

    return result


def get_sp500_tickers():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    table = pd.read_html(url)
    df = table[0]
    return df['Symbol'].tolist()


def save_tickers(tickers: list[str], index: str):
    newpath = "D:\\Data\\Programming\\GitHub\\StockScreener\\Data\\Indices"

    if not os.path.exists(newpath):
        os.makedirs(newpath)

    filepath = newpath + "\\" + index + ".txt"

    with open(filepath, "w") as file:
        for ticker in tickers:
            file.write(ticker + "\n")