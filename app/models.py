from flask_login import UserMixin
from app import mysql
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin):

    def __init__(self, id, username, email, password=None, google_id=None, profile_pic=None, created_at=None, updated_at=None, is_active=1, last_login=None):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.google_id = google_id
        self.profile_pic = profile_pic
        self.created_at = created_at
        self.updated_at = updated_at
        self.last_login = last_login

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
                id=user_data[0],
                username=user_data[1],
                email=user_data[2],
                password=user_data[3],
                google_id=user_data[4],
                profile_pic=user_data[5],
                created_at=user_data[6],
                updated_at=user_data[7],
                last_login=user_data[9]
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
                profile_pic=user_data[5],
                created_at=user_data[6],
                updated_at=user_data[7],
                last_login=user_data[9]
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
                profile_pic=user_data[5],
                created_at=user_data[6],
                updated_at=user_data[7],
                is_active=user_data[8],
                last_login=user_data[9]
            )
        return None

    @staticmethod
    def get_all():
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        cursor.close()
        return users
    def check_password(self, password):
        return check_password_hash(self.password, password)

    @staticmethod
    def create_user(username, email, password=None, google_id=None, profile_pic=None, is_active=1, last_login=None):
        cursor = mysql.connection.cursor()
        
        if password:
            password = generate_password_hash(password)
            
        sql = """INSERT INTO users (username, email, password, google_id, profile_pic, is_active, last_login) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (username, email, password, google_id, profile_pic, is_active, last_login))
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
            profile_pic=profile_pic,
            is_active=is_active,
            last_login=last_login
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

    def update_last_login(self):
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE users SET last_login = NOW() WHERE id = %s", (self.id,))
        mysql.connection.commit()
        cursor.close()

    def set_active(self):
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE users SET is_active = %s WHERE id = %s", (1, self.id))
        mysql.connection.commit()
        cursor.close()

    def set_inactive(self):
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE users SET is_active = %s WHERE id = %s", (0, self.id))
        mysql.connection.commit()
        cursor.close()

class Student():   
    def __init__(self, id, name, yearlevel, enrollmentStatus, program, college):
        self.id = id
        self.name = name
        self.yearlevel = yearlevel
        self.enrollmentStatus = enrollmentStatus
        self.program = program
        self.college = college

    @staticmethod
    def get_all():
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM student')
        students = cursor.fetchall()
        cursor.close()
        return students

    @staticmethod
    def get_by_id(student_id):
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM student WHERE id = %s', (student_id,))
        student_data = cursor.fetchone()
        cursor.close()
        
        if student_data:
            return Student(
                id=student_data[0],
                name=student_data[1],
                yearlevel=student_data[2],
                enrollmentStatus=student_data[3],
                program=student_data[4],
                college=student_data[5]
            )
        return None
    
    @staticmethod
    def add_student(name, yearlevel, enrollmentStatus, program, college):
        cursor = mysql.connection.cursor()
        sql = """INSERT INTO student (name, yearlevel, enrollmentStatus, program, college) 
                 VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(sql, (name, yearlevel, enrollmentStatus, program, college))
        mysql.connection.commit()
        
        student_id = cursor.lastrowid
        cursor.close()
        
        return Student(
            id=student_id,
            name=name,
            yearlevel=yearlevel,
            enrollmentStatus=enrollmentStatus,
            program=program,
            college=college
        )

    @staticmethod
    def update_student(student_id, name, yearLevel, enrollmentStatus, program, college):
        cursor = mysql.connection.cursor()
        sql = """UPDATE student SET name = %s, yearLevel = %s, enrollmentStatus = %s, program = %s, college = %s WHERE id = %s"""
        cursor.execute(sql, (name, yearLevel, enrollmentStatus, program, college, student_id))
        mysql.connection.commit()
        cursor.close()
        return True
    
    @staticmethod
    def delete_student(student_id):
        cursor = mysql.connection.cursor()
        sql = "DELETE FROM student WHERE id=%s"
        cursor.execute(sql, (student_id,))
        mysql.connection.commit()
        cursor.close()
        return True
    


class Program():
    def __init__(self, id,courseCode,name,college):
        self.id = id
        self.courseCode = courseCode
        self.name = name
        self.college = college

    @staticmethod
    def get_all():
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM program')
        programs = cursor.fetchall()
        cursor.close()
        return programs
    
    @staticmethod
    def get_by_id(program_id):
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM program WHERE id = %s', (program_id,))
        program = cursor.fetchone()
        cursor.close()
        if program:
            return Program(
                id=program[0],
                courseCode=program[1],
                name=program[2],
                college=program[3]
            )
        return None
    
    @staticmethod
    def add_program(courseCode, name, college):
        cursor = mysql.connection.cursor()
        sql = """INSERT INTO program (courseCode, name) 
                 VALUES (%s, %s, %s)"""
        cursor.execute(sql, (courseCode, name))
        mysql.connection.commit()
        
        program_id = cursor.lastrowid
        cursor.close()
        
        return Program(
            id=program_id,
            courseCode=courseCode,
            name=name,

        )
    

class College():
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @staticmethod
    def get_all():
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM college')
        colleges = cursor.fetchall()
        cursor.close()
        return colleges
    
    @staticmethod
    def get_by_id(college_id):
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM college WHERE id = %s', (college_id,))
        college = cursor.fetchone()
        cursor.close()
        if college:
            return College(
                id=college[0],
                name=college[1]
            )
        return None
    
    @staticmethod
    def add_college(name):
        cursor = mysql.connection.cursor()
        sql = """INSERT INTO college (name) 
                 VALUES (%s)"""
        cursor.execute(sql, (name,))
        mysql.connection.commit()
        
        college_id = cursor.lastrowid
        cursor.close()
        
        return College(
            id=college_id,
            name=name
        )