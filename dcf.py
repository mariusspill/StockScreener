# assumptions

growth_rate = 0.017
ev_ebitda_multiple = 7
cost_of_debt = 0.05
tax_rate = 0.25
treasury_10y = 0.015

beta = 1.3
market_return = 0.1
equity_value_assumption = 17500
debt_value_assumption = 15000

n = 5

ebit_assumption = {1: 5000,
                   2: 5200,
                   3: 5400,
                   4: 5500,
                   5: 5500}

da_assumption = {1:325,
                  2:330,
                  3:330,
                  4:320,
                  5:320}


capEx_assumptiion = {1:1550,
                     2:1550,
                     3:1500,
                     4:1500,
                     5:1500}

non_cash_increase = {1:180,
                     2:170,
                     3:160,
                     4:150,
                     5:145}
    

cash = 500
marketable_securities = 4500
short_term_debt = 3650
long_term_debt = 16540

shares_outstanding = 1000

#  https://www.youtube.com/watch?v=gLULdxrS-CU

def non_cash_working_capital(current_assets: int, cash: int, current_liabilities: int):
    return (current_assets - cash - current_liabilities)

def free_cash_flow(ebit: int, depreciation_and_amortization: int, capital_expenditures: int, increase_in_non_cash_working_capital: int, tax_rate = 0.25):
    return ((ebit * (1-tax_rate)) + depreciation_and_amortization - capital_expenditures - increase_in_non_cash_working_capital)

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


def equity_value(enterprise_value: int, cash: int, marketable_securities: int, short_term_debt: int, long_term_debt: int):
    return (enterprise_value + cash + marketable_securities - short_term_debt - long_term_debt)


def enterprise_value(discounted_cash_flow: dict, discounted_terminal_value):
    result = 0
    for values in discounted_cash_flow.values():
        result += values
    result += discounted_terminal_value
    return result

def share_price(equity_value: int, shares_outstanding: int):
    return equity_value / shares_outstanding


# calcutate FCF: 

cash_flow = dict()
for i in range(1, n + 1):
    cash_flow[i] = free_cash_flow(ebit_assumption[i],
                                  da_assumption[i],
                                  capEx_assumptiion[i],
                                  non_cash_increase[i])
print(cash_flow)

wacc = weighted_average_cost_of_capital(equity_value_assumption, debt_value_assumption, cost_of_working_equity(treasury_10y, beta, market_return), cost_of_debt)
print(wacc)

tv = terminal_Value(cash_flow[n], growth_rate, wacc, ebit_assumption[n] + da_assumption[n], ev_ebitda_multiple)
print(tv)

dfc = discounting_cashflows(wacc, cash_flow)
print(dfc)

dtv = discounting_terminal_value(wacc, tv, n)
print(dtv)

ev = enterprise_value(dfc, dtv)
print(ev)

eqv = equity_value(ev, cash, marketable_securities, short_term_debt, long_term_debt)
print(eqv)

sp = share_price(eqv, shares_outstanding)
print(sp)