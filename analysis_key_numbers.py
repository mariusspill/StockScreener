"""
Analysis of stocks by key numbers that are relevant for my strategy
"""

import yfinance as yf
import dbdata
import math
import sqlConnection as sql

lastYear = 2024




def average_net_income_5years(ticker: str):
    years = 5
    data = list()
    
    for i in range(years):
        data.append(dbdata.get_net_income(ticker, lastYear - i))

    sum = 0

    for income in data:
        sum += int(income)
    
    return (sum / years)


def income_growth_rate(ticker: str, year: int):
    lastYear = dbdata.get_net_income(ticker, year - 1)
    thisYear = dbdata.get_net_income(ticker, year)

    if thisYear < 0 and lastYear > 0:
        return - 1
    
    if lastYear < 0 and thisYear > 0:
        return 0

    return (thisYear / lastYear) - 1
    

def average_growth_rate_5years(ticker: str):
    sum = 0

    for year in range(lastYear - 4, lastYear + 1):
        rate = income_growth_rate(ticker, year)
        sum += rate

    return (sum / 5)


def variance_net_income_5years(ticker: str):
    years = 5
    data = list()
    
    for i in range(years):
        data.append(dbdata.get_net_income(ticker, lastYear - i))

    avrg = average_net_income_5years(ticker)

    result = 0

    for income in data:
        result += (income - avrg) ** 2 

    return (result / (years - 1))


def standard_deviation_net_income_5years(ticker: str):
    return math.sqrt(variance_net_income_5years(ticker))


def coefficient_of_variation_net_income_5years(ticker: str):
    return standard_deviation_net_income_5years(ticker) / average_net_income_5years(ticker)


def pe_income_average_5years(ticker: str):
    income = average_net_income_5years(ticker)
    marketCap = yf.Ticker(ticker).info["marketCap"]
    return round(marketCap / income, 4)