# def list_of_stocks2(ticker_list: str):
#     formatted_tickers = "', '".join(ticker_list)
#     sql.cursor.execute(f"""SELECT company_identifiers.ticker, income_statements.net_income, income_statements.year
#                    FROM Company INNER JOIN Company_Identifiers ON Company.id = Company_Identifiers.company_id
#                    INNER JOIN income_statements ON company.id = income_statements.company_id
#                    WHERE income_statements.year >= 2019
#                    AND company_identifiers.ticker IN ('{formatted_tickers}');""")
#     data = sql.cursor.fetchall()

#     data = pd.DataFrame(data, columns=('ticker', 'net_income', 'year'))

#     stock_list = dict()
#     mcaps = cch.get_market_caps()

#     for ticker in ticker_list:
#         stock_list[ticker] = Stock(ticker)
#         df = data[data['ticker'] == ticker]
#         income_sum = 0
#         growth_sum = 0
#         for i in range(2020, 2025):
#             try:
#                 inc = int(df[df['year'] == i]['net_income'].values[0])
#                 inc_ly = int(df[df['year'] == i - 1]['net_income'].values[0])
#                 stock_list[ticker].net_income[i] = inc
#                 income_sum += inc
#                 if inc >= 0 and inc_ly >= 0:
#                     growth_sum += inc / inc_ly - 1
#                 elif inc >= 0:
#                     growth_sum += 0
#                 else:
#                     growth_sum -= 1
#             except:
#                 growth_sum -= 1
#                 stock_list[ticker].net_income[i] = 0
#         average_growth = growth_sum / 5
#         average_income = income_sum / 5
#         stock_list[ticker].average_income_growth = average_growth

#         marketCap = mcaps[ticker]
       
#         stock_list[ticker].pe_5year_average = round(marketCap / average_income, 4)

#     return stock_list 
