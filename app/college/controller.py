from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from . import college_bp

from app.models import User,Student,Program,College
from app import client


@college_bp.route('/colleges')
def programs():
    colleges = College.get_all()
    return render_template('college/index.html', data=colleges)