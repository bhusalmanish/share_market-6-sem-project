
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model


st.title("  NEPSE : Stock Trend Prediction")
# Allow the user to upload their own data file
uploaded_file = st.file_uploader("Upload a CSV file with stock data", type=["csv"])
if uploaded_file is not None:
    # Read data from the uploaded CSV file
    df = pd.read_csv(uploaded_file)
     # Display the data in a table
    st.subheader("Data Table")
    st.write(df)

    # # Visualization
    # Moving Average of 100 Day
    st.subheader("Closing Price vs Time chart with 100 MA")

    df['Close'] = df['Close'].str.replace(',', '').astype(float)
    ma100 = df['Close'].rolling(100).mean()
    fig = plt.figure(figsize=(12, 6))
    plt.plot(ma100 ,'r', label = "100MA")
    plt.plot(df['Close'] , 'b' , label = 'Close price')
    plt.legend()

    st.pyplot(fig)
    
   #200MA
    st.subheader("Closing Price vs Time chart with 200 MA")
    ma200 = df['Close'].rolling(200).mean()
    fig = plt.figure(figsize=(12, 6))
    plt.plot(ma200, 'g', label = "200MA")
    plt.plot(df['Close'] , 'b' , label = 'Close price')
    plt.legend()

    st.pyplot(fig)

    # Stock close price
    st.subheader("Closing Price and 100DayMA & 200DayMA")
    fig = plt.figure(figsize=(12, 6))
    plt.plot(ma100 ,'r', label = "100MA")
    plt.plot(ma200, 'g', label = "200MA")
    plt.plot(df['Close'] , 'b' , label = 'Close price')
    plt.legend()

    st.pyplot(fig) 



      # SPliting Data into  Training and Testing
    data_training = pd.DataFrame(df['Close'][0:int(len(df)*0.70)])
    data_testing = pd.DataFrame(df['Close'][int(len(df)*0.70):int(len(df))])
    
    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler(feature_range=(0, 1))

    data_training_array = scaler.fit_transform(data_training)


#   already train data in model  so comment it here:
    # splting data into x-train and y-train
    # x_train = []
    # y_train = []
    # for i in range(100,data_training_array.shape[0]):
    #   x_train.append(data_training_array[i-100:i])
    #   y_train.append(data_training_array[i,0])
    # x_train, y_train = np.array(x_train),np.array(y_train)

    
    # load mymodel
    model = load_model("my_Stock.keras")  
    # Testing data
    past_100_days = data_training.tail(100)
    final_df = pd.concat([past_100_days, data_testing], ignore_index=True)
    input_data  = scaler.fit_transform(final_df)

    x_test = []
    y_test = []
    for i in range(100, input_data.shape[0]):
        x_test.append(input_data[i-100:i])
        y_test.append(input_data[i,0])

    x_test , y_test  = np.array(x_test), np.array(y_test)
    y_predicted = model.predict(x_test)
    scaler=scaler.scale_
    scale_factor = 1/scaler[0]
    y_predicted = y_predicted*scale_factor
    y_test = y_test*scale_factor


    # prediction vs Real Price
    st.header("Prediction vs Real Price")
    fig2= plt.figure(figsize=(12,6))

    plt.plot(y_test,'b', label= "Orginal Price")
    plt.plot(y_predicted, 'r', label = "Predicted Price")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.legend()
    st.pyplot(fig2)



