"""
Module provides functions to screen a list of stocks
"""

import yfinance as yf
import databases.dbdata as dbdata
import analysis.analysis_key_numbers as akn
import databases.sqlConnection as sql
import helpers.tickers as tickers
import pandas as pd
import caching.caching as cch


class Stock:
    ticker: str
    net_income: dict[int, int]
    earnings_growth: dict[int, float]
    average_income_growth: float
    average_income_5years: float
    pe_5year_average: float


    def __init__(self, ticker):
        self.ticker = ticker
        self.net_income = dict()
        self.earnings_growth = dict()
        self.screener = True


    def to_net_income(self, year, value):
        self.net_income[year] = value


    def calc_earnings_growth(self, year):
        lastYear = self.net_income[year - 1]
        thisYear = self.net_income[year]

        if thisYear < 0 and lastYear > 0:
            self.earnings_growth[year] = - 1
        elif lastYear < 0 and thisYear > 0:
            self.earnings_growth[year] =  0
        else:
            self.earnings_growth[year] = (thisYear / lastYear) - 1
        

    def calc_average_earnings_growth(self):
        sum = 0

        min_year = min(self.net_income.keys())
        years = self.net_income.keys()

        for year in years:
            if year != min_year:
                self.calc_earnings_growth(year)

        lastYear = max(self.net_income.keys())

        for year in range(lastYear - 4, lastYear + 1):
            try:
                rate = self.earnings_growth[year]
            except:
                rate = -1
            sum += rate

        self.average_income_growth = (sum / 5)


    def calc_income_average_5years(self):
        years = 5
        sum = 0

        earnings = self.net_income.values()

        for earning in earnings :
            sum += earning
            
        self.average_income_5years = (sum / years)


    def calc_pe_averaged_5years(self):
        income = self.average_income_5years
        mcaps = cch.get_market_caps()
        self.pe_5year_average = round(mcaps[self.ticker] / income, 4)



def print_analysis(tckrs: str):
    for ticker in tckrs:
        print()
        print(ticker)
        print(akn.average_growth_rate_5years(ticker))
        print(akn.pe_income_average_5years(ticker))


def list_of_stocks(ticker_list: str):
    formatted_tickers = "', '".join(ticker_list)
    sql.cursor.execute(f"""SELECT company_identifiers.ticker, income_statements.net_income, income_statements.year
                   FROM Company INNER JOIN Company_Identifiers ON Company.id = Company_Identifiers.company_id
                   INNER JOIN income_statements ON company.id = income_statements.company_id
                   WHERE income_statements.year >= 2019
                   AND company_identifiers.ticker IN ('{formatted_tickers}');""")
    data = sql.cursor.fetchall()

    stock_list = dict()

    for ticker in ticker_list:
        stock_list[ticker] = Stock(ticker)

    for entry in data:
        stock_list[entry[0]].to_net_income(entry[2], entry[1])

    for ticker in ticker_list:
        try:
            stock_list[ticker].calc_average_earnings_growth()
            stock_list[ticker].calc_income_average_5years()
            stock_list[ticker].calc_pe_averaged_5years()
        except:
            continue

    return stock_list


def screening(stock_list: dict[str, Stock], pe:int = 25):
    result_list = list()    
    pe = int(pe)

    for stock in stock_list.values():
        try:
            screen = True
            if stock.pe_5year_average >= pe or stock.pe_5year_average <= 0 or stock.average_income_growth < 0:
                screen = False
            for i in range(min(stock.net_income.keys()) + 1, max(stock.net_income.keys()) + 1):
                if stock.net_income[i] < 0:
                    screen = False
            if stock.average_income_growth < 0.05:
                screen = False

            if max(stock.net_income.values()) - min(stock.net_income.values()) > min(stock.net_income.values()) * 0.6:
                screen = False

            if screen:
                result_list.append(stock)
            
        except:
            continue

    i = 1
    for stock in result_list:
        print(i, stock.ticker, stock.average_income_growth, stock.pe_5year_average )
        i+=1

    return result_list


def Screening_as_dict(stock_list: dict[str, Stock], pe: int=25):
    screen = screening(stock_list, pe)
    result = dict()
    for element in screen:
        result[element.ticker] = (element.average_income_growth, element.pe_5year_average)
    return result
