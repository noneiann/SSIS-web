from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from . import student_bp

from app.models import User,Student
from app import client

from .forms import StudentForm

@student_bp.route('/index')
def index():
    students = Student.get_all()
    return render_template('student/index.html', data=students, studentform=StudentForm())


@student_bp.route('/add_student', methods=['POST'])
def add_student():
    data = request.get_json()
    form = StudentForm(formdata=None, data=data)
    if form.validate():
        Student.add_student(
            form.name.data,
            form.yearLevel.data,
            form.enrollmentStatus.data,
            form.program.data,
            form.college.data
        )
        flash('Student added successfully', 'success')
        return jsonify({'success': True, 'message': 'Student added successfully'}), 200
    else:
        return jsonify({'success': False, 'message': 'Validation failed', 'errors': form.errors}), 400
    

@student_bp.route('/update_student/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    form = StudentForm(formdata=None, data=data)
    if form.validate():
        try:
            Student.update_student(
                student_id,
                form.name.data,
                form.yearLevel.data,
                form.enrollmentStatus.data,
                form.program.data,
                form.college.data
            )
            return jsonify({'success': True, 'message': 'Student updated successfully'}), 200
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500
    return jsonify({'success': False, 'message': 'Validation failed', 'errors': form.errors}), 400       

@student_bp.route('/delete_student/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    try:
        Student.delete_student(student_id)
        return jsonify({'success': True, 'message': 'Student deleted successfully'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500     