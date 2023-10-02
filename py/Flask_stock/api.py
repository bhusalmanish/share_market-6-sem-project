from flask import Flask, request, render_template
import mysql.connector
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model

app = Flask(__name__)
model = load_model("my_Stock.keras")

# Establish a connection to your MySQL database
connection = mysql.connector.connect(
    host="localhost",  # Replace with your MySQL host
    user="root",  # Replace with your MySQL username
    password="",  # Replace with your MySQL password
    database="nepsestock"  # Replace with your MySQL database name
)

@app.route('/')
def index():
    # Fetch stock names from the database and pass them to the template
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT Name FROM stock")  # Replace with your table name
    stocks = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return render_template('index.html', stocks=stocks)

@app.route('/predict', methods=['POST'])
def predict():
    selected_stock = request.form.get('stock_name')
    
    # Fetch data for the selected stock from the database
    cursor = connection.cursor()
    query = f"SELECT Close FROM stock WHERE Name = '{selected_stock}'"  # Replace with your table name
    cursor.execute(query)
    selected_stock_data = [row[0] for row in cursor.fetchall()]
    cursor.close()
    
    # Preprocess data for prediction
    scaler = MinMaxScaler(feature_range=(0, 1))
    data_scaled = scaler.fit_transform(np.array(selected_stock_data).reshape(-1, 1))

    x_test = []
    for i in range(100, len(data_scaled)):
        x_test.append(data_scaled[i-100:i, 0])
    x_test = np.array(x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

    # Make predictions
    predicted_prices = model.predict(x_test)
    predicted_prices = scaler.inverse_transform(predicted_prices)
    
    # Get the last predicted price
    prediction_result = predicted_prices[-1][0]

    return render_template('result.html', prediction=prediction_result)

if __name__ == '__main__':
    app.run(debug=True)
