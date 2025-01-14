from flask import render_template, request, jsonify
from flask_login import login_required
from . import student_bp
from app.models import Student
from .forms import StudentForm

import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
@student_bp.route('/index')
@login_required
def index():
    form = StudentForm()
    students = Student.get_all()
    print(students)
    form.update_program_choices()
    return render_template('student/index.html', data=students, studentform=form)    

@student_bp.route('/add_student', methods=['POST'])
@login_required
def add_student():
    try:
        data = request.get_json()
        form = StudentForm(formdata=None, data=data)
        form.update_program_choices()
        
        if form.validate_on_submit():
            image = None
            if form.image.data:
                image = form.image.data
                
            Student.add_student(
                form.studentIdYear.data,
                form.studentIdNumber.data,
                form.name.data,
                form.yearLevel.data,
                form.enrollmentStatus.data,
                form.program.data,
                image
            )
            print(form.data)
            return jsonify({'success': True, 'message': 'Student added successfully'})
        return jsonify({'success': False, 'message': 'Validation failed', 
                       'errors': form.errors}), 400
    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@student_bp.route('/update_student/<string:student_id>', methods=['PUT'])
@login_required
def update_student(student_id):
    try:
        data = request.get_json()
        form = StudentForm(formdata=None, data=data)
        form.update_program_choices()
        updated_id = form.studentIdYear.data + '-' + form.studentIdNumber.data
        print(form.data)
        if form.validate_on_submit():
            image = None
            if form.image.data:
                image = form.image.data
            Student.update_student(
                student_id,
                updated_id,
                form.name.data,
                form.yearLevel.data,
                form.enrollmentStatus.data,
                form.program.data,
                image
            )
            return jsonify({'success': True, 'message': 'Student updated successfully'})
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
    


@student_bp.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400
        
    file = request.files['image']

    student_id = request.form.get('student_id')
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Optional: Validate file type
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    if not ('.' in file.filename and \
        file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
        return jsonify({'error': 'Invalid file type'}), 400

    try:
        # Upload to Cloudinary
        result = cloudinary.uploader.upload(
            file,
            folder="student_photos/",
            public_id=f"student_{student_id}",
            overwrite=True,  # Optional: organize uploads in folders
            transformation=[
                {'width': 200, 'height': 200, 'crop': 'auto','gravity' : 'auto'},
                {'quality': 'auto'}
            ]
        )
        
        return jsonify({
            'url': result['secure_url']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500