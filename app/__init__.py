import json
import os
import sqlite3

from flask import Flask
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
from config import SECRET_KEY, DB_USERNAME, DB_PASSWORD, DB_NAME, DB_HOST, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_DISCOVERY_URL
from flask_mysqldb import MySQL
from flask_dance.contrib.google import make_google_blueprint
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

from oauthlib.oauth2 import WebApplicationClient
import requests




# Initialize the CSRF protection
client = WebApplicationClient(GOOGLE_CLIENT_ID)
csrf = CSRFProtect()
mysql = MySQL()
login_manager = LoginManager()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    cloudinary.config( 
    cloud_name = "dljekfcbb", 
    api_key = "366459257666794", 
    api_secret = "db5G1g9XiBhV1P3BiZ-b06FPvIM", # Click 'View API Keys' above to copy your API secret
    secure=True
    )
    # Load configuration from environment variables
    app.config.from_mapping(
        SECRET_KEY=SECRET_KEY,       
        MYSQL_USER=DB_USERNAME,
        MYSQL_PASSWORD=DB_PASSWORD,
        MYSQL_DB=DB_NAME,
        MYSQL_HOST=DB_HOST,
        OAUTHLIB_INSECURE_TRANSPORT="1"
    )

    # Initialize CSRF protection
    csrf.init_app(app)
    mysql.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User  # Import here to avoid circular imports
        return User.get_by_id(user_id)

    @app.context_processor
    def utility_processor():
        def get_user_display_name():
            if current_user.is_authenticated:
                return current_user.username
            return
        return dict(user_display_name=get_user_display_name)
    from app.user import user_bp as user_blueprint
    from app.student import student_bp as student_blueprint
    from app.program import program_bp as program_blueprint
    from app.college import college_bp as college_blueprint
    app.register_blueprint(user_blueprint)
    app.register_blueprint(student_blueprint)
    app.register_blueprint(program_blueprint)
    app.register_blueprint(college_blueprint)

    # Upload an image
    upload_result = cloudinary.uploader.upload("https://res.cloudinary.com/demo/image/upload/getting-started/shoes.jpg",
                                           public_id="shoes")
    print(upload_result["secure_url"])

    # Optimize delivery by resizing and applying auto-format and auto-quality
    optimize_url, _ = cloudinary_url("shoes", fetch_format="auto", quality="auto")
    print(optimize_url)

    # Transform the image: auto-crop to square aspect_ratio
    auto_crop_url, _ = cloudinary_url("shoes", width=500, height=500, crop="auto", gravity="auto")
    print(auto_crop_url)
    return app


