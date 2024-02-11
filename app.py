import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from uptrend20SMA import nseCode
from datetime import datetime, timedelta

def dataframe():
    NS = '.NS'
    nsecode = nseCode()
    max = "max"
    today = datetime.now().date()
    # Format the date as YYYY-MM-DD
    dateform = "%Y-%m-%d"
    todays_date = today.strftime(dateform)
    previous_year_date = today - timedelta(days=365)
    previous_year_date = previous_year_date.strftime(dateform)
    start = previous_year_date
    print("start", start)
    end = todays_date
    print("end",end)
    print("list of shares for todays uptrend : \n",nsecode)
    for i in nsecode[:1]:
        ticker = yf.Ticker(i+NS)
        ###################################################
        history_data = ticker.history(start=start, end=end)
        # history_data = ticker.history(period=max)
        ###################################################

        # Print the historical data
        # print(history_data)
        df = history_data

        df["20_mavg"] = MA(df, period=20)
        df["50_mavg"] = MA(df, period=50)
        df["signal"] =np.where(df["20_mavg"]>df["50_mavg"],df["Close"].max(),-1)

        plt.figure(figsize=(16,8))
        plt.title(i)
        df["Close"].plot(legend=True)
        df["20_mavg"].plot(legend=True)
        df["50_mavg"].plot(legend=True)
        df["signal"].plot(legend=True)

        plt.show()

def MA(df,period):
    return df['Close'].rolling(period).mean()

dataframe()