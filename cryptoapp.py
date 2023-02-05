import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import yfinance as yf
import talib



# Map crypto to their yfinance tickers
keys = ['Bitcoin', 'Ethereum', 'SLP', 'XRP', 'Axie Infinity']
values = ['BTC-USD', 'ETH-USD', 'SLP-USD', 'XRP-USD', 'AXS-USD']

# Create the dictionary
crypto_dict = dict(zip(keys, values))



# Create the dropdown list
selected_option = st.selectbox("Select a cryptocurrency:", keys)
# Display the selected option
st.write("You selected:", selected_option)
st.title("Crypto Buy/Sell Recommendation ({})".format(selected_option))

#Create start and end dates
start_date = st.date_input("Select start date:")
end_date = st.date_input("Select end date:")

st.write("Start date:", start_date)
st.write("End date:", end_date)


@st.cache



def load_data():
    # load data from file or API
    def bg_color_text(val):
        color = 'green' if val == "buy" else 'red' if val =='sell' else 'white'
        return 'background-color: %s' % color
    btc = yf.Ticker(crypto_dict[selected_option]).history(start = start_date,end=end_date)
    df = pd.DataFrame(btc)
    df['Pct_change'] = df['Close'].pct_change()
    df['RSI'] = talib.RSI(df['Close'])
    # Create a new column based on the RSI values
    df['signal'] = 'hold'
    df.loc[df['RSI'] < 30, 'signal'] = 'buy'
    df.loc[df['RSI'] > 70, 'signal'] = 'sell'
    df.style.applymap(bg_color_text, subset=['signal']).background_gradient()

    return df


data = load_data()
st.write(data)

st.title('Closing price chart from {} to {}'.format(start_date,end_date))
st.line_chart(data['Close'])
st.title('RSI chart from {} to {}'.format(start_date,end_date))
st.line_chart(data['RSI'])
st.title('Percent Change Chart from {} to {}'.format(start_date,end_date))
st.line_chart(data['Pct_change'])
