# modules/honeypot.py
from flask import Blueprint, request, redirect, url_for, flash, render_template
from datetime import datetime
from .database import get_db_connection

bp = Blueprint('honeypot', __name__)

@bp.route('/admin_pannel')
def admin_pannel():
    log_attack(request)
    flash("Unauthorized access detected!", "danger")
    return redirect(url_for('auth.login'))

@bp.route('/show_attackers_data')
def show_attackers_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM attackers')
    attackers = cursor.fetchall()
    conn.close()
    return render_template('show_attackers.html', attackers=attackers)

def log_attack(request):
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    path = request.path
    referrer = request.referrer
    method = request.method
    query_string = request.query_string.decode()
    headers = str(dict(request.headers))
    form_data = str(dict(request.form))
    body = request.get_data(as_text=True)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO attackers (
                        ip_address, 
                        user_agent, 
                        timestamp, 
                        path, 
                        referrer, 
                        method, 
                        query_string, 
                        headers, 
                        form_data, 
                        body) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                   (ip_address, user_agent, timestamp, path, referrer, method, query_string, headers, form_data, body))
    conn.commit()
    conn.close()
