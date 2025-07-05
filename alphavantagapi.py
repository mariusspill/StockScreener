import requests
import os
import json

apikey = "54TJ9WUBHV8UU83V"

def get_income_statement_alphavantage(ticker: str):
    testPath = "./Data/RawData/" + ticker

    if os.path.exists(testPath):
        return {"False": "Data already exists"}


    url = "https://www.alphavantage.co/query"

    params = {
        "function": "INCOME_STATEMENT",
        "symbol": ticker,
        "apikey": apikey
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