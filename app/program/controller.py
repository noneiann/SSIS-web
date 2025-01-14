from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required
from . import program_bp
from app.models import Program, College
from .forms import ProgramForm


@program_bp.route('/programs')
@login_required
def programs():
    form = ProgramForm()
    programs = Program.get_all()
    print(programs)
    form.update_college_choices()
    return render_template('program/index.html', data=programs, programForm=form)

@program_bp.route('/add_program', methods=['POST'])
@login_required
def add_program():
    try:
        data = request.get_json()
        form = ProgramForm(formdata=None, data=data)
        form.update_college_choices()
        
        if form.validate():
            Program.add_program(
                form.courseCode.data,
                form.name.data,
                form.college.data
            )
            return jsonify({'success': True, 'message': 'Program added successfully'})
        return jsonify({'success': False, 'message': 'Validation failed', 
                       'errors': form.errors}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@program_bp.route('/update_program/<string:program_id>', methods=['PUT'])
@login_required
def update_program(program_id):
    try:
        data = request.get_json()
        form = ProgramForm(formdata=None, data=data)
        form.update_college_choices()
        
        if form.validate():
            Program.update_program(
                program_id,
                form.courseCode.data,
                form.name.data,
                form.college.data
            )
            return jsonify({'success': True, 'message': 'Program updated successfully'})
        return jsonify({'success': False, 'message': 'Validation failed', 
                       'errors': form.errors}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@program_bp.route('/delete_program/<string:program_id>', methods=['DELETE'])
@login_required
def delete_program(program_id):
    try:
        Program.delete_program(program_id)
        return jsonify({'success': True, 'message': 'Program deleted successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500