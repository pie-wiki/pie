from flask import Blueprint, request, redirect, url_for, session
from flask_themes2 import render_theme_template, get_theme

login_bp = Blueprint('login', __name__)

users = {
    'admin': 'password123',
    'user': 'passw0rd'
}

def get_current_theme():
    return get_theme('default')  # Replace with dynamic selection if needed

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            error = 'Invalid credentials. Please try again.'
    return render_theme_template(get_current_theme(), 'login.html', error=error)

@login_bp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login.login'))

