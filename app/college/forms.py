from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class CollegeForm(FlaskForm):
    abbreviation = StringField('Abbreviation', validators=[DataRequired()])  
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')