import requests
import os
import json

apikey = "54TJ9WUBHV8UU83V"

def get_income_statement_alphavantage(ticker: str):
    url = "https://www.alphavantage.co/query"

    params = {
        "function": "INCOME_STATEMENT",
        "symbol": "IBM",
        "apikey": "demo"
    }

    response = requests.get(url, params)

    data = response.json()

    return data


def save_json_raw(ticker: str, data: dict, type: str):
    newpath = "D:\\Data\\Programming\\GitHub\\StockScreener\\Data\\RawData\\" + ticker

    if not os.path.exists(newpath):
        os.makedirs(newpath)

    filepath = newpath + "\\" + ticker + "_" + type  + ".json"

    with open(filepath, "w") as file:
        file.write(json.dumps(data))