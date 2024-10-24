from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,SelectField
from wtforms.validators import DataRequired

class ProgramForm(FlaskForm):
    courseCode = StringField('Course Code', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    college = StringField('College')
    submit = SubmitField('Submit')