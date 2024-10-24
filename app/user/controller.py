from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from . import user_bp
from .forms import LoginForm, RegistrationForm
from app.models import User
from app import client

import json
import requests
from config import GOOGLE_DISCOVERY_URL, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

@user_bp.route('/')
@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('student.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user.google_id:
            flash('Google login required for emails registered through Google', 'error')
            return redirect(url_for('user.login'))  
        elif user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            user.update_last_login()
            user.set_active()
            return redirect(url_for('student.index'))
        flash('Invalid email or password', 'error')
    return render_template('login.html', form=form)

@user_bp.route('/login/google')
def google_login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    print(request_uri)
    return redirect(request_uri)

@user_bp.route('/login/google/callback')
def google_login_callback():
    try:
        if client is None:
            return "OAuth client not initialized.", 500
        
        code = request.args.get("code")
        if not code:
            flash("Authorization code missing.", "error")
            return redirect(url_for('user.login'))
            
        google_provider_cfg = get_google_provider_cfg()
        token_endpoint = google_provider_cfg["token_endpoint"]
        redirect_uri = url_for('user.google_login_callback', _external=True)
        token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=redirect_uri,
        code=code
    )
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
        )
        client.parse_request_body_response(json.dumps(token_response.json()))

        userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
        uri, headers, body = client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body)
        
        if not userinfo_response.json().get("email_verified"):
                flash("Google authentication failed: Email not verified.", "error")
                return redirect(url_for('user.login'))
                
        google_id = userinfo_response.json()["sub"]
        email = userinfo_response.json()["email"]
        picture = userinfo_response.json().get("picture")
        name = userinfo_response.json().get("given_name")
            
        user = User.get_by_google_id(google_id)
        if not user:
                # Check if email is already registered
                existing_user = User.get_by_email(email)
                if existing_user:
                    flash("Email already registered with different method.", "error")
                    return redirect(url_for('user.login'))
                
                # Create new user
                user = User.create_user(
                    username=email.split('@')[0],
                    email=email,
                    google_id=google_id,
                    profile_pic=picture
                )
            
        login_user(user)
        return redirect(url_for('student.index'))  
    except Exception as e:
        flash(f"Google authentication failed: {str(e)}", "error")
        return redirect(url_for('user.login'))



@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.get_by_email(form.email.data):
            flash('Email already registered', 'error')
            return render_template('register.html', form=form)
        
        User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('user.login'))
    return render_template('register.html', form=form)

@user_bp.route('/logout')
@login_required
def logout():
    user = current_user
    user.set_inactive()
    logout_user()
    return redirect(url_for('user.login'))