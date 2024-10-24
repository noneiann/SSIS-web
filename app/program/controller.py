from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from . import program_bp

from app.models import User,Student,Program
from app import client

from .forms import ProgramForm


@program_bp.route('/programs')
def programs():
    programs = Program.get_all()
    return render_template('program/index.html', data=programs, programForm = ProgramForm())

@program_bp.route('/add_program', methods=['POST'])
def add_program():
    data = request.get_json()
    form = ProgramForm(formdata=None, data=data)

    if form.validate():
        Program.add_program(
            form.courseCode.data,
            form.name.data,
            form.college.data
        )
        flash('Program added successfully', 'success')
        return jsonify({'success': True, 'message': 'Program added successfully'}), 200
    else:
        return jsonify({'success': False, 'message': 'Validation failed', 'errors': form.errors}), 400

