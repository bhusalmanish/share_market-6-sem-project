import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.title("Stock Trend Prediction")


# Allow the user to upload their own data file
uploaded_file = st.file_uploader("Upload a CSV file with stock data", type=["csv"])

if uploaded_file is not None:
    # Read data from the uploaded CSV file
    df = pd.read_csv(uploaded_file)

    # Display the data summary
    st.subheader("Data Summary")
    st.write(df.describe())

    # Visualization
    st.subheader("Closing Price vs Time Frame Chart")

    # Create a Matplotlib figure
    fig, ax = plt.subplots(figsize=( 14,7))
    ax.plot(df['Date'], df['Close'])  # Plotting 'Close' against 'Date'
    ax.set_xlabel("Date")
    ax.set_ylabel("Closing Price")
    ax.set_title("Closing Price vs Time Frame")

    # Display the Matplotlib figure using st.pyplot()
    st.pyplot(fig)

    # Display the data in a table
    st.subheader("Data Table")
    st.write(df)

    # Moving Average of 100 Day
    st.subheader("Closing Price vs Time chart with 100 MA")
    ma100 = df['Close'].rolling(100).mean()
    fig = plt.figure(figsize=(12, 6))
    plt.plot(ma100)
    plt.plot(df['Close'])
    st.pyplot(fig)

    # MA of 200 Day
    st.subheader("Closing Price vs Time Chart with 100 MA & 200 MA")
    ma100 = df['Close'].rolling(100).mean()
    ma200 = df['Close'].rolling(200).mean()

    fig = plt.figure(figsize=(12, 6))
    plt.plot(ma100)
    plt.plot(ma200)
    plt.plot(df['Close'])
    st.pyplot(fig)
