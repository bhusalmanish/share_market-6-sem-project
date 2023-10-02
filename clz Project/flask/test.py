@app.route('/adminUser', methods=['GET'])
def get_all_users_route():
    users = get_all_users()
    # Render a template or return JSON response with users data
    # ...
    return render_template('adminUser.html', users=users)

# Route to retrieve a specific user by ID
@app.route('/adminUser/<int:user_id>', methods=['GET'])
def get_user_by_id_route(user_id):
    user = get_user_by_id(user_id)
    # Render a template or return JSON response with user data
    # ...
    return render_template('user_detail.html', user=user)

# Route to update user information
@app.route('/adminUser/update/<int:user_id>', methods=['POST'])
def update_user_route(user_id):
    new_username = request.form['new_username']
    new_password = request.form['new_password']
    update_user(user_id, new_username, new_password)
    return "User updated successfully!"

# Route to delete a user by ID
@app.route('/adminUser/delete/<int:user_id>', methods=['POST'])
def delete_user_route(user_id):
    delete_user(user_id)
    return "User deleted successfully!"