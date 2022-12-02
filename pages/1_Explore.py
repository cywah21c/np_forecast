import streamlit as st

import requests
from pandas import DataFrame
from datetime import datetime

#import matplotlib.pyplot as plt
import plotly.graph_objects as go

#import plotly.figure_factory as ff
from plotly.subplots import make_subplots

from functions.utils import daily_price_historical

def view_data(coin,data_n,short_n,long_n,key):
    coin_df = daily_price_historical(symbol=coin, comparison_symbol='USD',limit=data_n,apiKey=key)
    # last 50 dates
    st.write('Symbol: %s' % coin)
    #st.dataframe(coin_df[-50:])
            
    # compute ewma
    close_df = coin_df[['close','timestamp']]
    close_df.loc[:,'short_ewma']= close_df['close'].ewm(span=short_n).mean()
    close_df.loc[:,'long_ewma']= close_df['close'].ewm(span=long_n).mean()
    #close_df.set_index('timestamp', inplace=True)
    close_df = close_df[['timestamp','close','short_ewma','long_ewma']]
    
    fig = make_subplots(
    rows=2, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.2,
    specs=[[{"type": "scatter"}],
           [{"type": "table"}]]
)
    
    fig.add_trace(
        go.Scatter(
            x=close_df["timestamp"],
            y=close_df["close"],
            mode="lines",
            name="close"
        ),
        row=1, col=1
    )


    fig.add_trace(
        go.Scatter(
            x=close_df["timestamp"],
            y=close_df["short_ewma"],
            mode="lines",
            name="short ewma"
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=close_df["timestamp"],
            y=close_df["long_ewma"],
            mode="lines",
            name="long ewma"
        ),
        row=1, col=1
    )

    sub_df = close_df[-20:]
    fig.add_trace(
        go.Table(
            header=dict(
                values=["Date", "Closing Price", "Short EWMA","Long EWMA"],
                font=dict(size=10),
                align="left"
            ),
            cells=dict(
                values=[sub_df[k].tolist() for k in sub_df.columns[0:]],
                align = "left")
        ),
        row=2, col=1
    )
    
    fig.update_layout(
        height=800,
        showlegend=True,
        title_text="Daily Close Prices",
        xaxis_title="Date", yaxis_title="US$"
    )

    #fig.show()
    st.plotly_chart(fig,theme="streamlit")

def main():     
    st.markdown("# Explore Historical Data")
    #st.sidebar.header("Menu")
    st.write(
        """
        To download and explore crypto cyrrency data, set the following parameters using the sliders and press **Run** button:

        * currency symbol
        * number of historical data points
        * number of days for short EWMA
        * number of days for long EWMA
        """
    )

    # get latest data prices
    coin = st.sidebar.selectbox(
        'Currency symbol',
        ('BTC', 'ETH', 'XRP', 'ADA', 'DOGE'))
    data_n = st.sidebar.slider('Number of historical data points:', 1000, 2000, 1500)
    st.sidebar.write('Symbol: %s' % coin)
    st.sidebar.write('data points: %d' % data_n)

    # set ewma days
    short_n = st.sidebar.slider('Number of days for short EWMA:', 1, 30, 7)
    long_n = st.sidebar.slider('Number of datys for long EWMA:', 1, 180, 21)
    st.sidebar.write('Short EWMA: %d days' % short_n)
    st.sidebar.write('Long EWMA: %d days' % long_n)

    # retrieve crypto compare api key from local .streamlit/secrets.toml
    CC_KEY = st.secrets.api_keys.crypto_compare

    if st.sidebar.button('Run'):
        df = view_data(coin,data_n,short_n,long_n,CC_KEY)
    else:
        st.sidebar.write('Click `Run` button to explore downloaded data')

if __name__ == "__main__":
    main()
