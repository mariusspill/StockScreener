import data as dt
import math



def average_net_income_5years(ticker: str):
    years = 5
    data = dt.read_netIncome(ticker, years)

    sum = 0

    for income in data.values():
        sum += int(income)
    
    return (sum / years)


def income_growth_rate(ticker: str, t=5):
    years = t
    dt.read_netIncome(ticker, years)

    


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