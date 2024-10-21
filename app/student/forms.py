from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired

class StudentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    yearLevel = StringField('Year Level', validators=[DataRequired()])
    enrollmentStatus = StringField('Enrollment Status', validators=[DataRequired()])
    program = StringField('program')
    college = StringField('college')
    submit = SubmitField('Submit')