import os
import argparse
import mysql.connector
import json
import datetime
from flask import Flask, render_template, request, session, redirect, url_for, send_file
from functools import wraps


app = Flask(__name__)
app.static_folder = 'static'
app.secret_key = 'TestSecretKey'

# disable cache
#app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Configure MySQL database connection
dbconfig = {
  "host": "18.222.251.81",
  "user": "root",
  "password": "~My123456",
  "database": "my_test"
}

# MySQL Connection Pool Handle
connection_pool = None


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            # User not logged in, redirected to login page
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# Routing of login page
@app.route('/login.html')
def login():
    return render_template('login.html')


# Login Post Request
@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']

    connection = connection_pool.get_connection()
    cursor = connection.cursor()

    # Verify username and password
    query = "SELECT * FROM table_users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()

    if not user:
        cursor.close()
        connection.close()
        return json.dumps({'result': 'error', 'message': 'Invalid username or password'})

    # Login successful, update last login time
    last_login_time = datetime.datetime.now()
    update_query = "UPDATE table_users SET last_login_time = %s WHERE username = %s"
    cursor.execute(update_query, (last_login_time, username))
    connection.commit()
    cursor.close()
    connection.close()

    # Login successful, store username in session
    session['username'] = username
    session['firstname'] = user[3]
    session['lastname'] = user[4]
    session['email'] = user[5]
    return json.dumps({'result': 'success'})


# Routing of registration page
@app.route('/register.html')
def register():
    return render_template('register.html')


# Register Post Request
@app.route('/register', methods=['POST'])
def register_post():
    username = request.form['username']
    password = request.form['password']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']

    connection = connection_pool.get_connection()
    cursor = connection.cursor()

    # Check if the username already exists
    query = "SELECT * FROM table_users WHERE username = %s"
    cursor.execute(query, (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        cursor.close()
        connection.close()
        return json.dumps({'result': 'error', 'message': 'Username already exists'})

    # Register a new user
    register_time = datetime.datetime.now()
    last_login_time = None  # The initial value here is None, indicating that you have not logged in yet
    query = "INSERT INTO table_users (username, password, firstname, lastname, email, register_time, last_login_time) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (username, password, firstname, lastname, email, register_time, last_login_time)
    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    connection.close()

    session['username'] = username
    session['firstname'] = firstname
    session['lastname'] = lastname
    session['email'] = email

    return json.dumps({'result': 'success'})


# Routing of the logout page
@app.route('/logout')
@app.route('/logout.html')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


# Routing on homepage
@app.route('/')
@app.route('/index.html')
@login_required
def index():
    firstname = session.get('firstname')
    lastname = session.get('lastname')
    email = session.get('email')
    return render_template('index.html', firstname=firstname, lastname=lastname, email=email)


@app.route('/upload', methods=['POST'])
#@login_required
def upload():
    file = request.files['file']
    if file:
        os.makedirs('temp', exist_ok=True)
        file.save('temp/' + file.filename)

        with open('temp/' + file.filename, 'r') as f:
            contents = f.read()
            words = contents.split()
            return json.dumps({'words': len(words), 'download_link': '/download/' + file.filename, 'download_filename': file.filename})
    return json.dumps({'words': 0, 'download_link': '#'})

    
@app.route('/download/<filename>')
#@login_required
def download(filename):
    return send_file(f'temp/{filename}', as_attachment=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mysql_host', type=str, default='18.222.251.81', help='mysql host')
    parser.add_argument('--mysql_pwd', type=str, default='~My123456', help='mysql host')
    args = parser.parse_args()
    if len(args.mysql_host):
        dbconfig['host'] = args.mysql_host
    if len(args.mysql_pwd):
        dbconfig['password'] = args.mysql_pwd
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="my_pool", pool_size=5, **dbconfig)

    app.jinja_env.auto_reload = True
    app.run(host='0.0.0.0', port=8080, debug=True)
