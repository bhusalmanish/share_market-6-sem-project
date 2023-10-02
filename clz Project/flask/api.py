# from flask import Flask, render_template, request, redirect, url_for, flash, session
# from flask_mysqldb import MySQL
# import pandas as pd
# from keras.models import load_model
# from sklearn.preprocessing import MinMaxScaler


# app = Flask(__name__)

# # Configure MySQL
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'NepseStock'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# mysql = MySQL(app)

# # Secret key for session management
# app.secret_key = 'your_secret_key'

# # Routes for signup, login, and logout
# @app.route('/aa')
# def index():
#     if 'logged_in' in session:
#         return redirect(url_for('dashboard'))
#     return 'Welcome to the Flask Login and Signup App <a href="signup.html">Signup</a> app'

# @app.route('/', methods=['GET', 'POST'])
# def signup():
#     if 'logged_in' in session:
#         return redirect(url_for('dashboard'))

#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         cursor = mysql.connection.cursor()
#         cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
#         mysql.connection.commit()
#         cursor.close()
#         flash('You are now registered and can log in', 'success')
#         return redirect(url_for('login'))
#     return render_template('signup.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if 'logged_in' in session:
#         return redirect(url_for('dashboard'))

#     if request.method == 'POST':
#         username = request.form['username']
#         password_candidate = request.form['password']
#         cursor = mysql.connection.cursor()
#         result = cursor.execute("SELECT * FROM users WHERE username = %s", [username])
#         if result > 0:
#             data = cursor.fetchone()
#             password = data['password']
#             user_status = data['status']

#             if password_candidate == password:
#                 session['logged_in'] = True
#                 session['username'] = username
#                 session['status'] = user_status
#                 flash('You are now logged in', 'success')
#                 return redirect(url_for('dashboard'))
#             else:
#                 error = 'Invalid login'
#                 return render_template('login.html', error=error)
#             cursor.close()
#         else:
#             error = 'Username not found'
#             return render_template('login.html', error=error)
#     return render_template('login.html')

# @app.route('/dashboard')
# def dashboard():
#     if 'logged_in' not in session:
#         return redirect(url_for('login'))
    
#     # Check if the user is an admin (status '1')
#     if session.get('status') == 1:
#         # Display admin dashboard
#         return render_template('adminDashboard.html')
#     else:
       

#         # Display regular user dashboard
#        db = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="",
#         database="NepseStock"
#          )

# # Load the pre-trained model
#        model = load_model("my_Stock.keras")
#        scaler = MinMaxScaler(feature_range=(0, 1))


#        cursor = db.cursor()
#        cursor.execute("SELECT Date, Close FROM your_table_name")
#        data = cursor.fetchall()
#        cursor.close()

#     # Convert data to a pandas DataFrame
#        df = pd.DataFrame(data, columns=["Date", "Close"])
#        df["Close"] = df["Close"].astype(float)
    
#     # Perform predictions
#     scaled_data = scaler.fit_transform(df["Close"].values.reshape(-1, 1))
#     x_test = []
#     for i in range(100, len(scaled_data)):
#            x_test.append(scaled_data[i-100:i, 0])
#            x_test = np.array(x_test)
#            x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
#     predictions = model.predict(x_test)
#     predictions = scaler.inverse_transform(predictions)

#     # Prepare data for HTML rendering
#     dates = df.iloc[100:, 0].values
#     actual_prices = df.iloc[100:, 1].values
#     predicted_prices = predictions.flatten()

#     return render_template('index.html', dates=dates, actual_prices=actual_prices, predicted_prices=predicted_prices)

#         return render_template('home.html')


# @app.route('/logout')
# def logout():
#     session.clear()
#     flash('You are now logged out', 'success')
#     return redirect(url_for('login'))

# @app.route('/adminStock', methods=['GET', 'POST'])
# def admin_stock():
#     if 'file' not in request.files:
#         return "No file part"
    
#     file = request.files['file']

#     if file.filename == '':
#      return render_template("adminStock.html")
    
#     if file:
#         df = pd.read_csv(file)

#         # Insert data into MySQL table
#         cursor = mysql.connection.cursor()
#         for _, row in df.iterrows():
#             cursor.execute(
#                 "INSERT INTO Stock (sn, Name, Date, Txn, MaxPrice, MinPrice, Close, Volume, Turnover, PreClose, Change, ChangePercent) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
#                 (row['sn'], row['Name'], row['Date'], row['Txn'], row['MaxPrice'], row['MinPrice'], row['Close'], row['Volume'], row['Turnover'], row['PreClose'], row['Change'], row['Change%']))
#         mysql.connection.commit()
#         cursor.close()

#         return "Data uploaded successfully!"
#     return render_template("adminStock.html")


# @app.route('/adminUser')
# def admin_user():
#     return render_template("adminUser.html")

# if __name__ == '__main__':
#     app.run(debug=True)



from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import pandas as pd
import numpy as np
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import mysql.connector

app = Flask(__name__)

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'NepseStock'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# Secret key for session management
app.secret_key = 'your_secret_key'

# Routes for signup, login, and logout
@app.route('/aa')
def index():
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))
    return 'Welcome to the Flask Login and Signup App <a href="signup.html">Signup</a> app'


@app.route('/', methods=['GET', 'POST'])
def signup():
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        mysql.connection.commit()
        cursor.close()
        flash('You are now registered and can log in', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']
        cursor = mysql.connection.cursor()
        result = cursor.execute("SELECT * FROM users WHERE username = %s", [username])
        if result > 0:
            data = cursor.fetchone()
            password = data['password']
            user_status = data['status']

            if password_candidate == password:
                session['logged_in'] = True
                session['username'] = username
                session['status'] = user_status
                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            cursor.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    # Check if the user is an admin (status '1')
    if session.get('status') == 1:
        # Display admin dashboard
        return render_template('adminDashboard.html')
    else:
        # Display regular user dashboard
        # db = mysql.connector.connect(
        #     host="localhost",
        #     user="root",
        #     password="",
        #     database="NepseStock"
        # )

        # Load the pre-trained model
        model = load_model("my_Stock.keras")
        scaler = MinMaxScaler(feature_range=(0, 1))

        # cursor = db.cursor()
        # cursor.execute("SELECT Date, Close FROM Stock")
        # data = cursor.fetchall()
        # cursor.close()

        # Convert data to a pandas DataFrame
        # df = pd.DataFrame(data, columns=["Date", "Close"])
        # df["Close"] = df["Close"].astype(float)

        # Perform predictions
        # scaled_data = scaler.fit_transform(df["Close"].values.reshape(-1, 1))
        # x_test = []
        # for i in range(100, len(scaled_data)):
        #     x_test.append(scaled_data[i-100:i, 0])
        # x_test = np.array(x_test)
        # x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
        # predictions = model.predict(x_test)
        # predictions = scaler.inverse_transform(predictions)

        # # Prepare data for HTML rendering
        # dates = df.iloc[100:, 0].values
        # actual_prices = df.iloc[100:, 1].values
        # predicted_prices = predictions.flatten()

        # return render_template('index.html', dates=dates, actual_prices=actual_prices, predicted_prices=predicted_prices)
        return render_template('index.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

@app.route('/adminStock', methods=['GET', 'POST'])
def admin_stock():
    # if 'file' not in request.files:
    #     return "No file part"
    
    # file = request.files['file']

    # if file.filename == '':
    #     return render_template("adminStock.html")
    
    # if file:
    #     df = pd.read_csv(file)

    #     # Insert data into MySQL table
    #     cursor = mysql.connection.cursor()
    #     for _, row in df.iterrows():
    #         cursor.execute(
    #             "INSERT INTO Stock (sn, Name, Date, Txn, MaxPrice, MinPrice, Close, Volume, Turnover, PreClose, Change, ChangePercent) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
    #             (row['sn'], row['Name'], row['Date'], row['Txn'], row['MaxPrice'], row['MinPrice'], row['Close'], row['Volume'], row['Turnover'], row['PreClose'], row['Change'], row['Change%']))
    #     mysql.connection.commit()
    #     cursor.close()

    #     return "Data uploaded successfully!"
    return render_template("adminStock.html")

@app.route('/adminUser')
def admin_user():
    return render_template("adminUser.html")

if __name__ == '__main__':
    app.run(debug=True)
