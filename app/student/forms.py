from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,SelectField
from wtforms.validators import DataRequired

class StudentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    yearLevel = SelectField('Year Level', choices=[('First Year','First Year'),('Second Year','Second Year'), ('Third Year','Third Year'), ('Fourth Year','Fourth Year') ], validators=[DataRequired()])
    enrollmentStatus = SelectField('Enrollment Status',choices=[('Enrolled','Enrolled'), ('Not Enrolled', 'Not Enrolled')], validators=[DataRequired()])
    program = StringField('program')
    college = StringField('college')
    submit = SubmitField('Submit')