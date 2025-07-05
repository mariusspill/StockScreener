import data as dt
import math



def average_net_income_5years(ticker: str):
    years = 5
    data = dt.read_netIncome(ticker, years)

    sum = 0

    for income in data.values():
        sum += int(income)
    
    return (sum / years)


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


