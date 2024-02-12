import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

def nseDetails():
    url = "https://chartink.com/screener/process"
    #latest uptrend 20 days SMA stocks
    condition = {"scan_clause": "( {cash} ( latest sma( close,20 ) > latest sma( close,50 ) and 1 day ago  sma( close,20 )<= 1 day ago  sma( close,50 ) and latest volume > 300000 ) )"}

    with requests.session() as s:
        r_data = s.get(url)
        soup = bs(r_data.content, "lxml")
        meta = soup.find("meta", {"name" : "csrf-token"})["content"]

        header = {"x-csrf-token" : meta}
        data = s.post(url, headers=header, data=condition).json()

        stock_list = pd.DataFrame(data["data"])

    df = pd.DataFrame(stock_list)
    nsecode =  df[['nsecode', 'name']].values
    return nsecode