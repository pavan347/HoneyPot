# modules/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .database import get_db_connection
from flask_bcrypt import Bcrypt
from config import SECRET_KEY

bcrypt = Bcrypt()

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        user = session.get('user')
        if user :
            return redirect(url_for('routes.index'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if email and password were provided
        if not email or not password:
            flash('Email and password are required!', 'danger')
            return redirect(url_for('auth.login'))

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.check_password_hash(user['password'], password):
            session['user'] = {'id': user['id'], 'username': user['username'], 'email': user['email']}
            flash('Logged in successfully!', 'success')
            return redirect(url_for('routes.index'))
        else:
            flash('Incorrect email or password.', 'danger')
            return redirect(url_for('auth.login'))

    return render_template('login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('auth.register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        if cursor.fetchone():
            flash('Email already exists. Please try a different one.', 'danger')
            conn.close()
            return redirect(url_for('auth.register'))

        cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                       (username, email, hashed_password))
        conn.commit()
        conn.close()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@bp.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))
