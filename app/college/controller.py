from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from . import college_bp

from app.models import User, Student, Program, College
from app import client

from .forms import CollegeForm

@college_bp.route('/colleges')
@login_required
def programs():
    colleges = College.get_all()
    return render_template('college/index.html', data=colleges, collegeForm=CollegeForm())

@college_bp.route('/add_college', methods=['POST'])
def add_college():
    try:
        data = request.get_json()
        form = CollegeForm(formdata=None, data=data)
        if form.validate():
            college = College.add_college(
                form.abbreviation.data,
                form.name.data
            )
            flash('College added successfully', 'success')
            return jsonify({'success': True, 'message': 'College added successfully'}), 200
        return jsonify({'success': False, 'message': 'Validation failed', 'errors': form.errors}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@college_bp.route('/update_college/<string:college_abbreviation>', methods=['PUT'])
def update_college(college_abbreviation):
    data = request.get_json()
    form = CollegeForm(formdata=None, data=data)
    if form.validate():
        try:
            College.update_college(
                college_abbreviation,
                form.abbreviation.data,
                form.name.data
            )
            return jsonify({'success': True, 'message': 'College updated successfully'}), 200
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500
    return jsonify({'success': False, 'message': 'Validation failed', 'errors': form.errors}), 400

@college_bp.route('/delete_college/<string:college_abbreviation>', methods=['DELETE'])
def delete_college(college_abbreviation):
    try:
        College.delete_college(college_abbreviation)
        return jsonify({'success': True, 'message': 'College deleted successfully'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
