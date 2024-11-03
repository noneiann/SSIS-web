from flask import render_template, request, jsonify
from flask_login import login_required
from . import student_bp
from app.models import Student
from .forms import StudentForm

@student_bp.route('/index')
@login_required
def index():
    form = StudentForm()
    students = Student.get_all()
    form.update_program_choices()
    return render_template('student/index.html', data=students, studentform=form)   

@student_bp.route('/add_student', methods=['POST'])
@login_required
def add_student():
    try:
        data = request.get_json()
        form = StudentForm(formdata=None, data=data)
        form.update_program_choices()
        
        if form.validate():
            Student.add_student(
                form.studentIdYear.data,
                form.studentIdNumber.data,
                form.name.data,
                form.yearLevel.data,
                form.enrollmentStatus.data,
                form.program.data
            )
            return jsonify({'success': True, 'message': 'Student added successfully'})
        return jsonify({'success': False, 'message': 'Validation failed', 
                       'errors': form.errors}), 400
    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': "There is already a student with that ID"}), 500

@student_bp.route('/update_student/<string:student_id>', methods=['PUT'])
@login_required
def update_student(student_id):
    try:
        data = request.get_json()
        form = StudentForm(formdata=None, data=data)
        form.update_program_choices()
        
        if form.validate():
            Student.update_student(
                student_id,
                form.name.data,
                form.yearLevel.data,
                form.enrollmentStatus.data,
                form.program.data
            )
            return jsonify({'success': True, 'message': 'Student updated successfully'})
        return jsonify({'success': False, 'message': 'Validation failed', 
                       'errors': form.errors}), 400
    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@student_bp.route('/delete_student/<string:student_id>', methods=['DELETE'])
@login_required
def delete_student(student_id):
    try:
        Student.delete_student(student_id)
        return jsonify({'success': True, 'message': 'Student deleted successfully'})
    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500