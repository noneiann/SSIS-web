from flask_login import UserMixin
from app import mysql
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin):
    def __init__(self, id, username, email, password=None, google_id=None, profile_pic=None):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.google_id = google_id
        self.profile_pic = profile_pic

    def get_id(self):
        return str(self.id)

    @staticmethod
    def get_by_id(user_id):
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
        user_data = cursor.fetchone()
        cursor.close()
        
        if user_data:
            return User(
                id=user_data[0],  # Assuming id is the first column
                username=user_data[1],  # Assuming username is the second column
                email=user_data[2],  # Assuming email is the third column
                password=user_data[3],  # Assuming password is the fourth column
                google_id=user_data[4],  # Assuming google_id is the fifth column
                profile_pic=user_data[5]  # Assuming profile_pic is the sixth column
            )
        return None

    @staticmethod
    def get_by_google_id(google_id):
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE google_id = %s', (google_id,))
        user_data = cursor.fetchone()
        cursor.close()
        
        if user_data:
            return User(
                id=user_data[0],
                username=user_data[1],
                email=user_data[2],
                password=user_data[3],
                google_id=user_data[4],
                profile_pic=user_data[5]
            )
        return None

    @staticmethod
    def get_by_email(email):
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user_data = cursor.fetchone()
        cursor.close()
        
        if user_data:
            return User(
                id=user_data[0],
                username=user_data[1],
                email=user_data[2],
                password=user_data[3],
                google_id=user_data[4],
                profile_pic=user_data[5]
            )
        return None

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @staticmethod
    def create_user(username, email, password=None, google_id=None, profile_pic=None):
        cursor = mysql.connection.cursor()
        
        if password:
            password = generate_password_hash(password)
            
        sql = """INSERT INTO users (username, email, password, google_id, profile_pic) 
                 VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(sql, (username, email, password, google_id, profile_pic))
        mysql.connection.commit()
        
        # Get the ID of the newly created user
        user_id = cursor.lastrowid
        cursor.close()
        
        return User(
            id=user_id,
            username=username,
            email=email,
            password=password,
            google_id=google_id,
            profile_pic=profile_pic
        )

    @staticmethod
    def print_table_schema():
        """Utility method to print the table schema for debugging"""
        cursor = mysql.connection.cursor()
        cursor.execute("DESCRIBE users")
        columns = cursor.fetchall()
        cursor.close()
        for column in columns:
            print(column)