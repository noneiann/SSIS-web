from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class StudentForm(FlaskForm):
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
    submit = SubmitField('Submit')

    def update_program_choices(self):
        from app.models import Program
        programs = Program.get_all()
        self.program.choices = [(str(prog[0]), f"{prog[1]} - {prog[2]}") for prog in programs]