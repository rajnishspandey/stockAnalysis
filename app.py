import numpy as np
import yfinance as yf
import plotly.graph_objects as go
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
    print("end", end)
    print("list of shares for today's uptrend:\n", nsecode)
    
    for i in nsecode[:]:
        ticker = yf.Ticker(i + NS)
        
        # Fetch historical data
        history_data = ticker.history(start=start, end=end)
        df = history_data

        # Calculate moving averages
        df["20_mavg"] = MA(df, period=20)
        df["50_mavg"] = MA(df, period=50)

        # Add signals to the dataframe
        df['signal'] = np.where(df['20_mavg'] > df['50_mavg'], 1.0, 0.0)
        df['position'] = df['signal'].diff()

        # Predictions based on the last signal
        last_signal = df['signal'].iloc[-1]
        if last_signal == 1.0:
            prediction = "Predicting an uptrend. Consider buying."
        elif last_signal == 0.0:
            prediction = "Predicting a downtrend. Consider selling."
        else:
            prediction = "No clear trend prediction."

        # Plot the data
        fig = go.Figure(data=[go.Candlestick(x=df.index,
                                             open=df['Open'],
                                             high=df['High'],
                                             low=df['Low'],
                                             close=df['Close'],
                                             name='Candlesticks'),
                              go.Scatter(x=df.index, y=df["20_mavg"], name='20-day MA'),
                              go.Scatter(x=df.index, y=df["50_mavg"], name='50-day MA'),
                              go.Scatter(x=df.index[df['position'] == 1], 
                                         y=df["20_mavg"][df['position'] == 1],
                                         mode='markers', 
                                         marker=dict(symbol='triangle-up', color='green', size=15),
                                         name='Buy Signal'),
                              go.Scatter(x=df.index[df['position'] == -1], 
                                         y=df["20_mavg"][df['position'] == -1],
                                         mode='markers', 
                                         marker=dict(symbol='triangle-down', color='red', size=15),
                                         name='Sell Signal')
                              ])

        fig.update_layout(title=i,
                          xaxis_title='Date',
                          yaxis_title='Price',
                          xaxis_rangeslider_visible=False,
                          annotations=[
                              dict(
                                  x=df.index[-1],
                                  y=df["Close"].iloc[-1],
                                  xref="x",
                                  yref="y",
                                  text=prediction,
                                  showarrow=True,
                                  arrowhead=7,
                                  ax=0,
                                  ay=-40
                              )
                          ])

        fig.show()

def MA(df, period):
    return df['Close'].rolling(period).mean()

dataframe()
