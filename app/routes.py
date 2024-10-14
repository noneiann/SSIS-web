from flask import Flask, redirect, url_for, session, request, jsonify
from authlib.integrations.flask_client import OAuth
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['GOOGLE_CLIENT_ID'] = 'your_google_client_id'
app.config['GOOGLE_CLIENT_SECRET'] = 'your_google_client_secret'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'your_mysql_user'
app.config['MYSQL_PASSWORD'] = 'your_mysql_password'
app.config['MYSQL_DB'] = 'auth_db'

# Initialize MySQL connection
db = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB']
)

# Initialize OAuth
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    redirect_uri='http://localhost:5000/auth/google/callback',
    client_kwargs={'scope': 'openid email profile'}
)

# Initialize LoginManager
login_manager = LoginManager(app)

class User(UserMixin):
    def __init__(self, id, email):
        self.id = id
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    result = cursor.fetchone()
    if result:
        return User(id=result[0], email=result[1])
    return None

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login')
def login():
    return app.send_static_file('login.html')

@app.route('/register')
def register():
    return app.send_static_file('register.html')

@app.route('/auth/google')
def auth_google():
    redirect_uri = url_for('auth_google_callback', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/auth/google/callback')
def auth_google_callback():
    token = google.authorize_access_token()
    user_info = google.parse_id_token(token)
    email = user_info['email']
    google_id = user_info['sub']

    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE google_id = %s", (google_id,))
    user = cursor.fetchone()

    if user is None:
        cursor.execute(
            "INSERT INTO users (email, google_id, is_google_account) VALUES (%s, %s, %s)",
            (email, google_id, 1)
        )
        db.commit()
        user_id = cursor.lastrowid
    else:
        user_id = user[0]

    session['user_id'] = user_id
    login_user(User(id=user_id, email=email))
    return redirect('/dashboard')

@app.route('/dashboard')
@login_required
def dashboard():
    return f"Welcome {current_user.email} to your dashboard!"

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect('/login')

@app.route('/register_user', methods=['POST'])
def register_user():
    email = request.form.get('email')
    password = request.form.get('password')

    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    if cursor.fetchone():
        return jsonify({'error': 'User already exists!'}), 400

    # Here, you should hash the password before storing it
    cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
    db.commit()

    return jsonify({'message': 'Registration successful!'}), 201

if __name__ == '__main__':
    app.run(debug=True)
