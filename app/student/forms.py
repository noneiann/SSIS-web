from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

class StudentForm(FlaskForm):
    studentIdYear = StringField('ID Number', validators=[DataRequired(), Length(min=4, max=4)])
    studentIdNumber = StringField(validators=[DataRequired(), Length(min=4, max=4)])    
    name = StringField('Name', validators=[DataRequired()])
    program = SelectField('Program', validators=[DataRequired()])
    yearLevel = SelectField('Year Level', 
                            choices=[('First Year', 'First Year'),
                                     ('Second Year', 'Second Year'), 
                                     ('Third Year', 'Third Year'), 
                                     ('Fourth Year', 'Fourth Year')], 
                            validators=[DataRequired()])
    enrollmentStatus = SelectField('Enrollment Status',
                                   choices=[('Enrolled', 'Enrolled'), 
                                            ('Not Enrolled', 'Not Enrolled')], 
                                   validators=[DataRequired()])
    image = FileField('Profile Picture', 
                      validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField('Submit')

    def update_program_choices(self):
        from app.models import Program
        programs = Program.get_all()
        self.program.choices = [(prog[0], f"{prog[0]} - {prog[2]}") for prog in programs]