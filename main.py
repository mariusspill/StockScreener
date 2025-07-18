import helpers.tickers as tickers
import apis.alphavantagapi as ava
import analysis.analysis_screening as ascreen
import databases.sqlConnection as sql

tckrs = tickers.getTickers("./helpers/list.txt")

# ascreen.print_analysis(tckrs)

def daily_fetch():
    ava.fetch_data()
    sql.fetch_sp500_from_alpha_advantage()

# daily_fetch()
