import helpers.tickers as tickers
import apis.alphavantagapi as ava
import analysis.analysis_screening as ascreen
import databases.sqlConnection as sql
import helpers.tickers as helpers
import caching.caching as cch
import webinterface.webmain as wm
import threading
import webinterface.data_transfer as dt

tckrs = tickers.getTickers("./helpers/list.txt")

def daily_fetch():
    ava.fetch_data()
    sql.fetch_sp500_from_alpha_advantage()


def daily_cache():
    cch.cache_market_caps(tckrs)


def mainFunction():
    dt.shared.set_list(ascreen.Screening_as_dict(ascreen.list_of_stocks(tckrs)))
    

if __name__ == "__main__":
    t1 = threading.Thread(target=wm.runFlask)
    t2 = threading.Thread(target=mainFunction)

    t1.start()
    t2.start()
    t1.join()
    t2.join()