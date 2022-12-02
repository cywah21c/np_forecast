import streamlit as st

import neuralprophet

import pickle

import requests
import pandas as pd
from pandas import DataFrame
from datetime import datetime

import matplotlib.pyplot as plt

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from functions.utils import daily_price_historical

def predict(coin,limit,key):
    # download latest prices
    latest_df = daily_price_historical(symbol=coin, comparison_symbol='USD', limit=limit, apiKey=key)
    latest_df = latest_df[['timestamp','close']]
    latest_df = latest_df.rename(columns={"timestamp": "ds", "close": "y"})

    # load neurapprohet model
    filepath = f'./models/np_{coin.lower()}.pkl'
    model = pickle.load(open(filepath, 'rb'))

    # predcit prices
    future = model.make_future_dataframe(latest_df, periods=3)
    forecast_df = model.predict(future)
    forecast_df = forecast_df[['ds','y','yhat1','yhat2','yhat3']]
    raw_df = forecast_df[:7][['ds','y']]
    raw_df = raw_df.rename(columns={"ds": "date", "y": "actual"})
    
    predict_df = forecast_df[-3:][['ds','yhat1','yhat2','yhat3']]
    predict_df = predict_df.fillna(0)
    predict_df['predicted'] = predict_df.yhat1.fillna(0) + predict_df.yhat2.fillna(0) + predict_df.yhat3.fillna(0)
    predict_df = predict_df[['ds','predicted']]
    predict_df = predict_df.rename(columns={"ds": "date"})
    #predict_df.set_index('date', inplace=True)
    
    all_df  = pd.concat([raw_df,predict_df])
    #all_df.set_index('date', inplace=True)
    
    #st.dataframe(all_df) 
    
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.2, 
        specs=[[{"type": "scatter"}],
               [{"type": "table"}]]
    )
    
    fig.add_trace(
        go.Scatter(
            x=all_df["date"],
            y=all_df["actual"],
            line=dict(color="#9FE2BF"),
            mode="lines",
            name="actual"
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=all_df["date"],
            y=all_df["predicted"],
            line=dict(color="#CD5C5C",dash="dot"),
            mode="lines",
            name="predicted"
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Table(
            header=dict(
                values=["Date","Actual","Predicted"],
                font=dict(size=10),
                align="left"
            ),
            cells=dict(
                values=[all_df[k].tolist() for k in all_df.columns[0:]],
                align = "left")
        ),
        row=2, col=1
    )
    
    fig.update_layout(
        height=800,
        showlegend=True,
        title_text="Predicted Close Prices for next 3 Days",
        xaxis_title="Date", yaxis_title="US$"
    )

    #fig.show()
    st.plotly_chart(fig, theme="streamlit")

def main():

    st.markdown("# Predict Future Prices")
    #st.sidebar.header("Menu")
    st.write("Select a crypto currency for prediction")

    # get prices for past 7 days
    coin = st.sidebar.selectbox(
        'Currency symbol',
        ('BTC', 'ETH', 'XRP', 'ADA', 'DOGE'))
    st.sidebar.write('Symbol: %s' % coin)

    # retrieve crypto compare api key from local .streamlit/secrets.toml
    CC_KEY = st.secrets.api_keys.crypto_compare
    limit = 6
    if st.sidebar.button('Run'):
        predict(coin,limit,CC_KEY)
    else:
        st.sidebar.write('Click `Run` button for 3-day forecast')

if __name__ == "__main__":
    main()
