
@app.route('/adminStock/add_company', methods=['POST'])
def add_company_route():
    name = request.form['name']
    add_company_name(name)
    return "Company name added successfully!"

# Route to upload stock data from CSV file
@app.route('/adminStock/upload_data', methods=['POST'])
def upload_stock_data_route():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']

    if file.filename == '':
        return "No selected file"
    
    upload_stock_data(file)
    return "Stock data uploaded successfully!"

# Route to retrieve all stock data
@app.route('/adminStock', methods=['GET'])
def get_all_stock_data_route():
    stock_data = get_all_stock_data()
    # Render a template or return JSON response with stock data
    # ...
    return render_template('adminStock.html', stock_data=stock_data)

# Route to update stock data by ID
@app.route('/adminStock/update/<int:stock_id>', methods=['POST'])
def update_stock_data_route(stock_id):
    new_data = {
        'sn': request.form['sn'],
        'Name': request.form['Name'],
        'Date': request.form['Date'],
        'Txn': request.form['Txn'],
        'MaxPrice': request.form['MaxPrice'],
        'MinPrice': request.form['MinPrice'],
        'Close': request.form['Close'],
        'Volume': request.form['Volume'],
        'Turnover': request.form['Turnover'],
        'PreClose': request.form['PreClose'],
        'Change': request.form['Change'],
        'ChangePercent': request.form['ChangePercent']
    }
    update_stock_data(stock_id, new_data)
    return "Stock data updated successfully!"

# Route to delete stock data by ID
@app.route('/adminStock/delete/<int:stock_id>', methods=['POST'])
def delete_stock_data_route(stock_id):
    delete_stock_data(stock_id)
    return "Stock data deleted successfully!"
