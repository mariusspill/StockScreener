import pandas as pd
import numpy as np
import matplotlib as plt 

import sys
from pathlib import Path

# Add the project root (parent of analysis/) to the module search path
sys.path.append(str(Path(__file__).resolve().parent.parent))


import helpers.tickers as tickers
import analysis.analysis_key_numbers as akn
import yfinance as yf



tckrs = tickers.getTickers("./helpers/list.txt")

data = {}

for tckr in tckrs:
    data[tckr] = {}
    data[tckr]["income_growth"] = akn.average_growth_rate_5years(tckr)
    data[tckr]["marketCap"] = yf.Ticker(tckr).info['marketCap']

df = pd.DataFrame(data)
df = df.T

X = np.c_[df["marketCap"]]
y = np.c_[df["income_growth"]]

# Visualize the data
df.plot(kind='scatter', x="marketCap", y='income_growth')
plt.show()

print(df)
