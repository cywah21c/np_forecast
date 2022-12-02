import streamlit as st
import requests
from pandas import DataFrame
from datetime import datetime

# fn: download daily close prices
@st.cache
def daily_price_historical(symbol,comparison_symbol,limit=1,aggregate=1,exchange='',apiKey='',metric="close"):
    url = 'https://min-api.cryptocompare.com/data/histoday?fsym={}&tsym={}&limit={}&aggregate{}&api_key={}'\
            .format(symbol.upper(), comparison_symbol.upper(), limit, aggregate, apiKey)
    if exchange:
        url += '&e={#}'.format(exchange)
    page = requests.get(url)
    data = page.json()['Data']
    #series = [x[metric] for x in data]
    df = DataFrame(data)
    df['timestamp'] = [datetime.fromtimestamp(d) for d in df.time]
    df = df.drop(columns=['time','conversionType','conversionSymbol'])
    return df
