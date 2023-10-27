import time
from flask import Flask, render_template, request, redirect, url_for
from prometheus_client import start_http_server, Counter
import time
import logging
from tinydb import TinyDB, Query

# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO)

# Define a counter metric
requests_counter = Counter('myapp_requests', 'Total number of requests')

app = Flask(__name__)

# Define a dictionary of valid login credentials and corresponding dashboard pages
valid_credentials = {
    'user1': 'password1',
    'user2': 'password2',
    'user3': 'password3',
    'user4': 'password4'
}

dashboard_pages = {
    'user1': 'dashboard1.html',
    'user2': 'temp.html',
    'user3': 'dashboard3.html',
    'user4': 'dashboard4.html'
}

# Initialize the database
db = TinyDB('db.json')

# Insert sample user data (replace with your actual data)
User = Query()
db.insert({'username': 'user1', 'password': 'password1'})
db.insert({'username': 'user2', 'password': 'password2'})
db.insert({'username': 'user3', 'password': 'password3'})
db.insert({'username': 'user4', 'password': 'password4'})

@app.route('/')
def index():
    return "Welcome to the Login Page!"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check credentials against the database
        user = db.get((User.username == username) & (User.password == password))

        if user:
            return redirect(url_for('dashboard', username=username))
        else:
            return "Invalid login credentials. Please try again."

    return render_template('login.html')

@app.route('/background_task')
def background_task():
    # Simulate a background task that takes 15 seconds
    time.sleep(15)
    return "Background Task Completed"

@app.route('/trigger_error')
def trigger_error():
    # Simulate an error
    try:
        result = 1 / 0
    except Exception as e:
        logging.error(str(e))
        return "Error occurred: " + str(e)

@app.route('/dashboard/<username>')
def dashboard(username):
    # Simulate a delay of 10-20 seconds
    time.sleep(1)

    return render_template(dashboard_pages.get(username))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

