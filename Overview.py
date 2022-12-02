import streamlit as st

def main():
    st.set_page_config(
        page_title="Crypto Current Price Forescast",
    )

    st.write("# Crypto Currency Price Prediction Demo")

    st.sidebar.success("Select from the menu")

    st.markdown(
        """
        This site demonstrates Streamlit deployment of machine learning 
        models for the prediction of crypto currency prices.
        A [NeuralProhet](https://neuralprophet.com/) model was built for 
        each of BTC, ETH, XRP, ADA and DOGE crypto currencies with data 
        available from [CryptoCompare](https://www.cryptocompare.com/).

        **Select from the menu on the sidebar**:
        - Overview: View this page
        - Explore: Explore historical daily crypto currency data from CryptoCompare
        - Forecast: Predict crypto currency prices for next three days
    """
    )

if __name__ == "__main__":
    main()
