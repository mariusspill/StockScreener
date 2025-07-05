import data

# assumptions

growth_rate = 0.03      # gdp or industry growth in %
ev_ebitda_multiple = 7  # peer group, check formula soon
cost_of_debt = 0.05
tax_rate = 0.25
treasury_10y = 0.015

beta = 1.3
market_return = 0.1
equity_value_assumption = 17500
debt_value_assumption = 15000

cash = 500
marketable_securities = 4500
short_term_debt = 3650
long_term_debt = 16540

shares_outstanding = 1000

#  https://www.youtube.com/watch?v=gLULdxrS-CU

def non_cash_working_capital(current_assets: int, cash: int, current_liabilities: int):
    return (current_assets - cash - current_liabilities)


def free_cash_flow(ebit: int, depreciation_and_amortization: int, capital_expenditures: int, increase_in_non_cash_working_capital: int, tax_rate = 0.21):
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


def cash_flow_prediction(cash_flow: dict, growth_rate: float, n: int = 7, last_cash_flow_multiplicative: float = 1.0):
    currentyear = max(cash_flow.keys())

    last_cashflow = cash_flow[currentyear] * last_cash_flow_multiplicative

    estimates = dict()

    for i in range(1, n):
        estimates[currentyear + i] = last_cashflow * (1 + growth_rate) ** i

    return estimates


def cost_of_working_equity(treasury: float, beta: float, market_return: float):
    return treasury + (beta * (market_return - treasury))


def weighted_average_cost_of_capital(equity: int, debt: int, cost_of_equity: float, cost_of_debt: float, tax_rate : float = 0.25):
    a = (equity / (equity + debt)) * cost_of_equity
    b = ((debt / (equity + debt)) * cost_of_debt) * (1 - tax_rate)
    return a + b 


def perpetuity_growth(fcfn: int, g: float, wacc: float):
    return (fcfn *  (1 + g)) / (wacc - g)


def exit_multiple(ebitdan: int, ev_ebitda_multiple: int):
    return ebitdan * ev_ebitda_multiple


def terminal_Value(fcfn: int, g: float, wacc: float, ebitdan: int, ev_ebitda_multiple: int):
    return ((perpetuity_growth(fcfn, g, wacc) + exit_multiple(ebitdan, ev_ebitda_multiple))/2)


def discounting_cashflows(wacc:  float, cashflows: dict[int, int]):
    discount_factor = dict()
    for i in range(1, len(cashflows.keys()) + 1):
        discount_factor[i] = 1 / ((1 + wacc) ** i)

    discounted_cashflow = dict()

    for i in range(1, len(cashflows.keys()) + 1):
        discounted_cashflow[i] = cashflows[i] * discount_factor[i]

    return discounted_cashflow


def discounting_terminal_value(wacc: float, tv: int, n: int):
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


def calculate_free_cash_flow_ebit_formula(ticker: str, year:int ):
    ebit = data.get_ebit(ticker, year)
    depreciationAndAmortization = data.get_depreciation_and_amortization(ticker, year)
    capex = data.get_capitalExpenditure(ticker, year)

    lyTotalAsset = data.get_total_current_assets(ticker, year - 1)
    lyTotalCash = data.get_cash_and_cash_equivalents(ticker, year - 1)
    lyTotalLiabilities = data.get_total_current_liabilities(ticker, year - 1)

    totalAsset = data.get_total_current_assets(ticker, year)
    totalCash = data.get_cash_and_cash_equivalents(ticker, year)
    totalLiabilities = data.get_total_current_liabilities(ticker, year)

    ly_non_cash_working_capital = non_cash_working_capital(int(lyTotalAsset), int(lyTotalCash), int(lyTotalLiabilities))
    this_non_cash_working_capital = non_cash_working_capital(int(totalAsset), int(totalCash), int(totalLiabilities)) 
    net_change_in_non_cash_working_capital =  ly_non_cash_working_capital - this_non_cash_working_capital 

    fcf = free_cash_flow(int(ebit), int(depreciationAndAmortization), int(capex), net_change_in_non_cash_working_capital)
    return fcf


def calculate_free_cash_flow_cfo_formula(ticker: str, year: int):
    operating_cashflow = data.get_operating_cashflow(ticker, year)
    capex = data.get_capitalExpenditure(ticker, year)

    return int(operating_cashflow) - int(capex)


def calculate_free_cash_flow(ticker:str, year: int):
    return calculate_free_cash_flow_cfo_formula(ticker, year)

