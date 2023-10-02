import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import streamlit as st

st.title("Stock Trend Prediction")

user_input = st.text_input("Enter The Stock ", 'AAPL')

# Error handling for fetching data
try:
    # Use yfinance to fetch data
    df = yf.download(user_input, start='2015-01-01', end='2020-12-31')

    if not df.empty:
        # Display the data summary
        st.subheader("Data From 2015 - 2022")
        st.write(df.describe())

        # Visualization
        st.subheader("Closing Price vs Time Frame Chart")

        # Create a Matplotlib plot
        plt.figure(figsize=(12, 6))
        plt.plot(df.index, df['Close'])  # Plotting 'Close' against the index (time)
        plt.xlabel("Date")
        plt.ylabel("Closing Price")
        plt.title("Closing Price vs Time Frame")

        # Display the Matplotlib plot using st.pyplot()
        st.pyplot()

        # Display the data in a table
        st.subheader("Data Table")
        st.write(df)
    else:
        st.error("No data available for the provided stock symbol.")

except Exception as e:
    st.error(f"An error occurred: {str(e)}")
