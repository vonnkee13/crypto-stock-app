import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import datetime



# Map crypto to their yfinance tickers
keys = ['Bitcoin', 'Ethereum', 'SLP', 'XRP', 'Axie Infinity']
values = ['BTC-USD', 'ETH-USD', 'SLP-USD', 'XRP-USD', 'AXS-USD']

# Create the dictionary
crypto_dict = dict(zip(keys, values))



# Create the dropdown list
selected_option = st.selectbox("Select a cryptocurrency:", keys)
# Display the selected option
st.title("Crypto Buy/Sell Recommendation ({})".format(selected_option))

#Create start and end dates


default_start_date = datetime.datetime(2022, 1, 1)
today = datetime.datetime.today()
start_date = st.date_input("Select start date:",default_start_date)
end_date = st.date_input("Select end date:",today)

st.write("Start date:", start_date)
st.write("End date:", end_date)

#Select number of days for rolling window
wdw = int(st.number_input("Number of rolling window days:",value = 3, step = 1))




def load_data():
    global wdw
    # load data from file or API
    def bg_color_text(val):
        color = 'green' if val == "buy" else 'red' if val =='sell' else 'white'
        return 'background-color: %s' % color
    btc = yf.Ticker(crypto_dict[selected_option]).history(start = start_date,end=end_date)
    df = pd.DataFrame(btc)
    df['Pct_change'] = df['Close'].pct_change()

    # Calculate the difference between today's close and yesterday's close
    delta = df["Close"].diff()

    # Create two arrays to store the gain and loss
    gain = np.zeros_like(delta)
    loss = np.zeros_like(delta)

    # Fill the arrays with the gains and losses
    for i in range(1, len(delta)):
        if delta[i] > 0:
            gain[i] = delta[i]
        else:
            loss[i] = -delta[i]

    gain = pd.DataFrame(gain)
    loss = pd.DataFrame(loss)
    # Calculate the 14-day average of gains and losses
    avg_gain = gain.rolling(window=wdw).mean()
    avg_loss = loss.rolling(window=wdw).mean()

    # Calculate the relative strength (RS)
    RS = avg_gain / avg_loss

    # Calculate the RSI
    RSI = 100 - (100 / (1 + RS))

    # Add the RSI to the dataframe
    df["RSI"] = np.array(RSI)

    # Create a new column based on the RSI values
    df['signal'] = 'hold'
    df.loc[df['RSI'] < 30, 'signal'] = 'buy'
    df.loc[df['RSI'] > 70, 'signal'] = 'sell'
    df.style.applymap(bg_color_text, subset=['signal']).background_gradient()

    return df


data = load_data()

st.title("{} price data from {} to {}".format(selected_option,start_date,end_date))
st.write(data)

st.title('Closing price chart from {} to {}'.format(start_date,end_date))
st.line_chart(data['Close'])
st.title('RSI chart from {} to {} based on {}-day rolling window'.format(start_date,end_date,wdw))
st.line_chart(data['RSI'])
st.title('Percent Change Chart from {} to {}'.format(start_date,end_date))
st.line_chart(data['Pct_change'])
