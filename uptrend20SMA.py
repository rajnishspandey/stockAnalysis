import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

def nseCode():
    url = "https://chartink.com/screener/process"
    #latest uptrend 20 days SMA stocks
    condition = {"scan_clause": "( {cash} ( latest close >= latest sma( close,20 ) and latest rsi( 14 ) > 55 and latest adx di positive( 14 ) > latest adx di negative( 14 ) and latest adx( 14 ) >= 30 and latest macd line( 26,12,9 ) > latest macd signal( 26,12,9 ) and latest adx di positive( 14 ) >= latest adx( 14 ) and latest volume >= 50000 and latest volume > latest sma( latest close , 20 ) and latest close - 1 candle ago close / 1 candle ago close * 100 > 3 and latest close >= 300 and market cap > 2000 ) ) "}

    with requests.session() as s:
        r_data = s.get(url)
        soup = bs(r_data.content, "lxml")
        meta = soup.find("meta", {"name" : "csrf-token"})["content"]

        header = {"x-csrf-token" : meta}
        data = s.post(url, headers=header, data=condition).json()

        stock_list = pd.DataFrame(data["data"])
        # print(stock_list)

    # print(stock_list)

    df = pd.DataFrame(stock_list)
    nsecode = df["nsecode"].values
    return nsecode
    