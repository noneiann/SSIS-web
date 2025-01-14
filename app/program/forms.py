from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class ProgramForm(FlaskForm):
    courseCode = StringField('Course Code', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    college = SelectField('College', validators=[DataRequired()], choices=[]) 
    submit = SubmitField('Submit')

    def update_college_choices(self):
        from app.models import College
        colleges = College.get_all()
        self.college.choices = [(college[0], college[1]) for college in colleges]