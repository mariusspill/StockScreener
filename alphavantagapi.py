import requests
import os
import json
import tickers

apikey = "54TJ9WUBHV8UU83V"
apikey2 = "9OJZQ19WTKV3SDT8"
apikey3 = "Z263ODOPE6WZ4706"

def get_testData(function: str):

    url = "https://www.alphavantage.co/query"

    params = {
        "function": function,
        "symbol": "IBM",
        "apikey": "demo"
    }



    response = requests.get(url, params)

    data = response.json()

    return data


def get_income_statement_alphavantage(ticker: str, key: str = apikey):
    testPath = "./Data/RawData/" + ticker

    if os.path.exists(testPath) and os.path.exists(testPath + "/" + ticker + "_incomeStatement.json"):
        return {"False": "Data already exists"}


    url = "https://www.alphavantage.co/query"

    params = {
        "function": "INCOME_STATEMENT",
        "symbol": ticker,
        "apikey": key
    }



    response = requests.get(url, params)

    data = response.json()

    return data


def get_balance_sheet_alphavantage(ticker: str, key: str = apikey):
    testPath = "./Data/RawData/" + ticker

    if os.path.exists(testPath) and os.path.exists(testPath + "/" + ticker + "_balanceSheet.json"):
        return {"False": "Data already exists"}


    url = "https://www.alphavantage.co/query"

    params = {
        "function": "BALANCE_SHEET",
        "symbol": ticker,
        "apikey": key
    }



    response = requests.get(url, params)

    data = response.json()

    return data


def get_cash_flow_alphavantage(ticker: str, key: str = apikey):
    testPath = "./Data/RawData/" + ticker

    if os.path.exists(testPath) and os.path.exists(testPath + "/" + ticker + "_cashFlow.json"):
        return {"False": "Data already exists"}


    url = "https://www.alphavantage.co/query"

    params = {
        "function": "CASH_FLOW",
        "symbol": ticker,
        "apikey": key
    }



    response = requests.get(url, params)

    data = response.json()

    return data


def save_json_raw(ticker: str, data: dict, type: str):
    if "Note" in data.keys() or "Information" in data.keys() or "False" in data.keys():
        return

    newpath = "D:\\Data\\Programming\\GitHub\\StockScreener\\Data\\RawData\\" + ticker

    if not os.path.exists(newpath):
        os.makedirs(newpath)

    filepath = newpath + "\\" + ticker + "_" + type  + ".json"

    with open(filepath, "w") as file:
        file.write(json.dumps(data))


def fetch_data():
    tckrs = tickers.getTickers("./Data/Indices/s&p500.txt")

    for ticker in tckrs:
        cf = get_income_statement_alphavantage(ticker)
        save_json_raw(ticker, cf, "incomeStatement")