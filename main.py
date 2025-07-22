import helpers.tickers as tickers
import apis.alphavantagapi as ava
import analysis.analysis_screening as ascreen
import databases.sqlConnection as sql
import helpers.tickers as helpers
import caching.caching as cch

tckrs = tickers.getTickers("./helpers/list.txt")

def daily_fetch():
    ava.fetch_data()
    sql.fetch_sp500_from_alpha_advantage()


def daily_cache():
    cch.cache_market_caps(tckrs)


ascreen.screening(ascreen.list_of_stocks(tckrs))
