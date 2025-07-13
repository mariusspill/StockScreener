import alphavantagedata as dt
import math


lastYear = 2024


def average_net_income_5years(ticker: str):
    years = 5
    data = dt.read_netIncome(ticker, years)

    sum = 0

    for income in data.values():
        sum += int(income)
    
    return (sum / years)


def income_growth_rate(ticker: str, year: int):
    lastYear = int(dt.get_netIncome(ticker, year - 1))
    thisYear = int(dt.get_netIncome(ticker, year))

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
    data = dt.read_netIncome(ticker, years)
    avrg = average_net_income_5years(ticker)

    result = 0

    for income in data.values():
        result += (int(income) - avrg) ** 2 

    return (result / (years - 1))


def standard_deviation_net_income_5years(ticker: str):
    return math.sqrt(variance_net_income_5years(ticker))


def coefficient_of_variation_net_income_5years(ticker: str):
    return standard_deviation_net_income_5years(ticker) / average_net_income_5years(ticker)


def pe_income_average_5years(ticker: str):
    income = average_net_income_5years(ticker)
    marketCap = dt.get_marketCap(ticker)
    return round(marketCap / income, 4)