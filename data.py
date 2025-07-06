import csv
import os
import json
import pandas as pd

lastYear = 2024

def append_to_financial_data(file: str, ticker: str, year: int, metric: str, value):
    with open(file, mode="a") as file:
        file.write("\n" + ticker + ", " + str(year) + ", " + metric + ", " + str(value))

def append_to_financial_data_by_company(file: str):
    pass

def read_netIncome(tckr: str, max = 50)-> dict:
    with open("./Data/RawData/" + tckr + "/" + tckr + "_incomeStatement.json", "r") as file:
        data = json.load(file)
    
    result = dict()

    for i in range(min(len(data["annualReports"]), max)):
        year = data["annualReports"][i]["fiscalDateEnding"][0:4]
        value = data["annualReports"][i]["netIncome"]
        result[year] = value

    return result


def get_ebit(tckr: str, year: int):
    with open("./Data/RawData/" + tckr + "/" + tckr + "_incomeStatement.json", "r") as file:
        data = json.load(file)

    return data["annualReports"][lastYear - year]["ebit"]


def get_depreciation_and_amortization(tckr: str, year: int):
    with open("./Data/RawData/" + tckr + "/" + tckr + "_incomeStatement.json", "r") as file:
        data = json.load(file)

    return data["annualReports"][lastYear - year]["depreciationAndAmortization"]


def get_capitalExpenditure(tckr: str, year: int):
    with open("./Data/RawData/" + tckr + "/" + tckr + "_cashFlow.json", "r") as file:
        data = json.load(file)

    return data["annualReports"][lastYear - year]["capitalExpenditures"]


def get_total_current_assets(tckr: str, year: int):
    with open("./Data/RawData/" + tckr + "/" + tckr + "_balanceSheet.json", "r") as file:
        data = json.load(file)

    return data["annualReports"][lastYear - year]["totalCurrentAssets"]


def get_cash_and_cash_equivalents(tckr: str, year: int):
    with open("./Data/RawData/" + tckr + "/" + tckr + "_balanceSheet.json", "r") as file:
        data = json.load(file)

    return data["annualReports"][lastYear - year]["cashAndShortTermInvestments"]


def get_total_current_liabilities(tckr: str, year: int):
    with open("./Data/RawData/" + tckr + "/" + tckr + "_balanceSheet.json", "r") as file:
        data = json.load(file)

    return data["annualReports"][lastYear - year]["totalCurrentLiabilities"]


def get_operating_cashflow(tckr: str, year: int):
    with open("./Data/RawData/" + tckr + "/" + tckr + "_cashFlow.json", "r") as file:
        data = json.load(file)

    return data["annualReports"][lastYear - year]["operatingCashflow"]


def get_short_term_debt(tckr: str, year: int):
    with open("./Data/RawData/" + tckr + "/" + tckr + "_balanceSheet.json", "r") as file:
        data = json.load(file)

    return data["annualReports"][lastYear - year]["shortTermDebt"]


def get_long_term_debt(tckr: str, year: int):
    with open("./Data/RawData/" + tckr + "/" + tckr + "_balanceSheet.json", "r") as file:
        data = json.load(file)

    return data["annualReports"][lastYear - year]["longTermDebt"]    


def get_interest_expense(tckr: str, year: int):
    with open("./Data/RawData/" + tckr + "/" + tckr + "_incomeStatement.json", "r") as file:
        data = json.load(file)

    return data["annualReports"][lastYear - year]["interestExpense"]


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