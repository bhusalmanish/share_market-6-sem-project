# Inside your Flask app

# Function to add a new company name
def add_company_name(name):
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO S_company (Name) VALUES (%s)", [name])
    mysql.connection.commit()
    cursor.close()

# Function to upload stock data from CSV file
def upload_stock_data(file):
    df = pd.read_csv(file)

    cursor = mysql.connection.cursor()
    for _, row in df.iterrows():
        cursor.execute(
            "INSERT INTO N_stock (sn, Name, Date, Txn, MaxPrice, MinPrice, Close, Volume, Turnover, PreClose, Change, ChangePercent) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (row['sn'], row['Name'], row['Date'], row['Txn'], row['MaxPrice'], row['MinPrice'], row['Close'], row['Volume'], row['Turnover'], row['PreClose'], row['Change'], row['Change%']))
    mysql.connection.commit()
    cursor.close()

# Function to retrieve all stock data
def get_all_stock_data():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM StockData")
    stock_data = cursor.fetchall()
    cursor.close()
    return stock_data

# Function to update stock data by ID
def update_stock_data(stock_id, new_data):
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE N_stock SET sn=%s, Name=%s, Date=%s, Txn=%s, MaxPrice=%s, MinPrice=%s, Close=%s, Volume=%s, Turnover=%s, PreClose=%s, Change=%s, ChangePercent=%s WHERE id=%s",
                   (new_data['sn'], new_data['Name'], new_data['Date'], new_data['Txn'], new_data['MaxPrice'], new_data['MinPrice'], new_data['Close'], new_data['Volume'], new_data['Turnover'], new_data['PreClose'], new_data['Change'], new_data['ChangePercent'], stock_id))
    mysql.connection.commit()
    cursor.close()

# Function to delete stock data by ID
def delete_stock_data(stock_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM N_stock WHERE id=%s", [stock_id])
    mysql.connection.commit()
    cursor.close()
