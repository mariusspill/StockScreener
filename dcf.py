"""
Basic DCF Model like the one used by warren buffett
"""


import alphavantagedata
import yfinance as yf

# assumptions

growth_rate = 0.02      # gdp or industry growth in %
ev_ebitda_multiple = 7  # peer group, check formula soon

tax= 0.21
market_return = 0.1

last_year = 2024
n = 7

#  https://www.youtube.com/watch?v=gLULdxrS-CU

def non_cash_working_capital(current_assets: int, cash: int, current_liabilities: int):
    return (current_assets - cash - current_liabilities)


def free_cash_flow(ebit: int, depreciation_and_amortization: int, capital_expenditures: int, increase_in_non_cash_working_capital: int, tax_rate = tax):
    return ((ebit * (1-tax_rate)) + depreciation_and_amortization - capital_expenditures - increase_in_non_cash_working_capital)



def cash_flow_growth(cash_flows: dict):
    cf_growth = dict()
    past = None
    for year in cash_flows.keys():
        if past != None:
            cf_growth[year] = (cash_flows[year] / past) - 1
        past = cash_flows[year]
    
    return cf_growth


def average_cash_flow_growth(cash_flow_growth: dict):
    sum = 0
    for keys in cash_flow_growth.keys():
        sum += cash_flow_growth[keys]

    avrg = sum / len(cash_flow_growth.keys())
    return(avrg)


def cash_flow_prediction(cash_flow: dict, growth_rate: float = 0.0, n: int = n + 1, last_cash_flow_multiplicative: float = 1.0):
    currentyear = max(cash_flow.keys())

    last_cashflow = cash_flow[currentyear] * last_cash_flow_multiplicative

    growth_rate = average_cash_flow_growth(cash_flow_growth(cash_flow))

    estimates = dict()

    for i in range(1, n):
        estimates[currentyear + i] = last_cashflow * (1 + growth_rate) ** i

    return estimates


def cost_of_working_equity(treasury: float, beta: float, market_return: float):
    return treasury + (beta * (market_return - treasury))


def weighted_average_cost_of_capital(equity: int, debt: int, cost_of_equity: float, cost_of_debt: float, tax_rate : float = tax):
    a = (equity / (equity + debt)) * cost_of_equity
    b = ((debt / (equity + debt)) * cost_of_debt) * (1 - tax_rate)
    return a + b 


def perpetuity_growth(fcfn: int, g: float, wacc: float):
    return (fcfn *  (1 + g)) / (wacc - g)


def exit_multiple(ebitdan: int, ev_ebitda_multiple: int):
    return ebitdan * ev_ebitda_multiple


def terminal_Value(fcfn: int, g: float, wacc: float):

    # just using perpetuity_growth for now

    return perpetuity_growth(fcfn, g, wacc)


def discounting_cashflows(wacc:  float, cashflows: dict[int, int]):
    discount_factor = dict()
    for i in range(1, len(cashflows.keys()) + 1):
        discount_factor[i] = 1 / ((1 + wacc) ** i)

    discounted_cashflow = dict()

    for i in range(1, len(cashflows.keys()) + 1):
        discounted_cashflow[i + last_year] = float(cashflows[i + last_year] * discount_factor[i])

    return discounted_cashflow


def discounting_terminal_value(wacc: float, tv: int, n: int = n):
    dicount_factor = 1 / ((1 + wacc)**n)
    return tv * dicount_factor


def enterprise_value(discounted_cash_flow: dict, discounted_terminal_value):
    result = 0
    for values in discounted_cash_flow.values():
        result += values
    result += discounted_terminal_value
    return result


def equity_value(enterprise_value: int, cash: int, marketable_securities: int, short_term_debt: int, long_term_debt: int):
    return (enterprise_value + cash + marketable_securities - short_term_debt - long_term_debt)


def share_price(equity_value: int, shares_outstanding: int):
    return equity_value / shares_outstanding



# automated for individual stock

def calculate_free_cash_flow_ebit_formula(ticker: str, year:int ):
    ebit = alphavantagedata.get_ebit(ticker, year)
    depreciationAndAmortization = alphavantagedata.get_depreciation_and_amortization(ticker, year)
    capex = alphavantagedata.get_capitalExpenditure(ticker, year)

    lyTotalAsset = alphavantagedata.get_total_current_assets(ticker, year - 1)
    lyTotalCash = alphavantagedata.get_cash_and_cash_equivalents(ticker, year - 1)
    lyTotalLiabilities = alphavantagedata.get_total_current_liabilities(ticker, year - 1)

    totalAsset = alphavantagedata.get_total_current_assets(ticker, year)
    totalCash = alphavantagedata.get_cash_and_cash_equivalents(ticker, year)
    totalLiabilities = alphavantagedata.get_total_current_liabilities(ticker, year)

    ly_non_cash_working_capital = non_cash_working_capital(int(lyTotalAsset), int(lyTotalCash), int(lyTotalLiabilities))
    this_non_cash_working_capital = non_cash_working_capital(int(totalAsset), int(totalCash), int(totalLiabilities)) 
    net_change_in_non_cash_working_capital =  ly_non_cash_working_capital - this_non_cash_working_capital 

    fcf = free_cash_flow(int(ebit), int(depreciationAndAmortization), int(capex), net_change_in_non_cash_working_capital)
    return fcf


def calculate_free_cash_flow_cfo_formula(ticker: str, year: int):
    operating_cashflow = alphavantagedata.get_operating_cashflow(ticker, year)
    capex = alphavantagedata.get_capitalExpenditure(ticker, year)

    return int(operating_cashflow) - int(capex)


def calculate_free_cash_flow(ticker:str, year: int):
    return calculate_free_cash_flow_cfo_formula(ticker, year)


def fcf_timeline(ticker:str, starting_year:int, end_year:int) -> dict:
    result = dict()

    for year in range(starting_year, end_year + 1):
        result[year] = calculate_free_cash_flow(ticker, year)

    return result


def calculate_debt(ticker: str, year: int):
    return (int(alphavantagedata.get_long_term_debt(ticker, year)) + int(alphavantagedata.get_short_term_debt(ticker, year)))


def calculate_equity_cost(ticker: str, year: int):
    rf = yf.Ticker("^TNX").history().loc['2025-07-02']["Open"] / 100
    rf = round(rf, 5)
    # rf = 0.07
    beta = yf.Ticker(ticker).info["beta"]
    rm = market_return

    return rf + beta * (rm - rf)
    

def calculate_cost_of_debt(ticker: str, year: int, tax_rate: float = tax):
    total_debt = calculate_debt(ticker, year)
    interest_expense = alphavantagedata.get_interest_expense(ticker,year)

    return ((int(interest_expense) / int(total_debt)) * (1 - tax_rate))


def calculate_wacc(ticker: str, year: int):
    equity = yf.Ticker(ticker).info["marketCap"]
    debt = calculate_debt(ticker, year)

    equity_cost = calculate_equity_cost(ticker, year)
    debt_cost = calculate_cost_of_debt(ticker, year)

    return weighted_average_cost_of_capital(equity, debt, equity_cost, debt_cost)



def calculate_terminal_value(ticker: str, year: int):
    free_cash_flow = fcf_timeline(ticker, year - 4, year)
    free_cash_flow_prediction = cash_flow_prediction(free_cash_flow)

    return terminal_Value(free_cash_flow_prediction[max(free_cash_flow_prediction.keys())], growth_rate, calculate_wacc(ticker, year))


def calculate_discounted_cash_flow(ticker: str, year: int):
    free_cash_flow = fcf_timeline(ticker, year - 4, year)
    free_cash_flow_prediction = cash_flow_prediction(free_cash_flow)

    return discounting_cashflows(calculate_wacc(ticker, year), free_cash_flow_prediction)


def calculate_discounted_terminal_value(ticker: str, year: int):
    return discounting_terminal_value(calculate_wacc(ticker, year), calculate_terminal_value(ticker, year))


def calculate_enterprise_value(ticker: str, year: int):
    return enterprise_value(calculate_discounted_cash_flow(ticker, 2024), calculate_discounted_terminal_value(ticker, 2024))


def calculate_equity_value(ticker: str, year: int):
    ev = calculate_enterprise_value(ticker, year)
    cash = int(alphavantagedata.get_cash_and_cash_equivalents(ticker, year))
    total_debt = calculate_debt(ticker, year)
    return equity_value(ev, cash, 0, total_debt, 0)


def calculate_share_price(ticker: str, year: int):
    return share_price(calculate_equity_value(ticker, year), yf.Ticker(ticker).info["sharesOutstanding"])


def dfc(ticker):
    return calculate_share_price(ticker, last_year)
