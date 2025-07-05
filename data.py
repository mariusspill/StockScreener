import csv
import os
import json

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