from flask import Flask, redirect, url_for, render_template
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
import os
import mysql.connector

# Load environment variables
load_dotenv()

# Initialize the CSRF protection
csrf = CSRFProtect()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # Load configuration from environment variables
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY"),
        MYSQL_USER=os.getenv("DB_USERNAME"),
        MYSQL_PASSWORD=os.getenv("DB_PASSWORD"),
        MYSQL_DB=os.getenv("DB_NAME"),
        MYSQL_HOST=os.getenv("DB_HOST"),
    )

    # Initialize CSRF protection
    csrf.init_app(app)

    # Define your routes
    @app.route('/')
    def index():
        return render_template('index.html')  # Assuming you have an index.html

    @app.route('/login')
    def login():
        return render_template('login.html')

    @app.route('/register')
    def register():
        return render_template('register.html')

    @app.route('/login_user', methods=['POST'])
    def login_user():
        email = request.form['email']
        password = request.form['password']
        # Your logic for logging in users goes here
        return redirect(url_for('index'))  # Redirect after successful login

    @app.route('/register_user', methods=['POST'])
    def register_user():
        email = request.form['email']
        password = request.form['password']
        # Your logic for registering users goes here
        return redirect(url_for('index'))  # Redirect after successful registration

    return app
