import csv
import os

def append_to_financial_data(file: str, ticker: str, year: int, metric: str, value):
    with open(file, mode="a") as file:
        file.write("\n" + ticker + ", " + str(year) + ", " + metric + ", " + str(value))

def append_to_financial_data_by_company(file: str):
    pass
