from flask import Flask, render_template, url_for
from datetime import datetime, timedelta
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
from uptrend20SMA import nseCode
from near20sma import nseDetails

app = Flask(__name__)

def MA(df, period):
    return df['Close'].rolling(period).mean()

def generate_plot(stock_code, stock_name):
    NS = '.NS'
    today = datetime.now().date()
    dateform = "%Y-%m-%d"
    todays_date = today.strftime(dateform)
    previous_year_date = today - timedelta(days=365)
    previous_year_date = previous_year_date.strftime(dateform)
    start = previous_year_date
    end = todays_date

    ticker = yf.Ticker(stock_code + NS)
    history_data = ticker.history(start=start, end=end)
    df = history_data

    df["20_mavg"] = MA(df, period=20)
    df["50_mavg"] = MA(df, period=50)
    df['signal'] = np.where(df['20_mavg'] > df['50_mavg'], 1.0, 0.0)
    df['position'] = df['signal'].diff()

    last_signal = df['signal'].iloc[-1]
    if last_signal == 1.0:
        prediction = "Predicting an uptrend. Consider buying."
    elif last_signal == 0.0:
        prediction = "Predicting a downtrend. Consider selling."
    else:
        prediction = "No clear trend prediction."

    fig = go.Figure(data=[
        go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='Candlesticks'),
        go.Scatter(x=df.index, y=df["20_mavg"], name='20-day MA'),
        go.Scatter(x=df.index, y=df["50_mavg"], name='50-day MA'),
        go.Scatter(x=df.index[df['position'] == 1], y=df["20_mavg"][df['position'] == 1],
                   mode='markers', marker=dict(symbol='triangle-up', color='green', size=15), name='Buy Signal'),
        go.Scatter(x=df.index[df['position'] == -1], y=df["20_mavg"][df['position'] == -1],
                   mode='markers', marker=dict(symbol='triangle-down', color='red', size=15), name='Sell Signal')
    ])

    fig.update_layout(title=stock_code + ' - ' + stock_name,  # Updated title to include stock_name
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

    return fig

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/uptrend')
def uptrend20sma():
    try:
        nsecodes = nseCode()

        # Extract stock codes and names from nseCode() output
        stock_codes = [stock[0] for stock in nsecodes]
        stock_names = [stock[1] for stock in nsecodes]

        plots = []

        for stock_code, stock_name in nsecodes:
            fig = generate_plot(stock_code, stock_name)  # Pass stock_name to generate_plot
            plots.append(fig.to_html(full_html=False))

        return render_template('uptrend20sma.html', stock_codes=stock_codes, stock_names=stock_names, plots=plots)
    except Exception:
        message = "There is no data in the filter today"
        return render_template('uptrend20sma.html', message=message)

@app.route('/near20sma')
def near20sma():
    try:
        nsecodes = nseDetails()

        # Extract stock codes and names from nseCode() output
        stock_codes = [stock[0] for stock in nsecodes]
        stock_names = [stock[1] for stock in nsecodes]

        plots = []

        for stock_code, stock_name in nsecodes:
            fig = generate_plot(stock_code, stock_name)  # Pass stock_name to generate_plot
            plots.append(fig.to_html(full_html=False))

        return render_template('near20sma.html', stock_codes=stock_codes, stock_names=stock_names, plots=plots)
    except Exception:
        message = "There is no data in the filter today"
        return render_template('near20sma.html', message=message)
      
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
