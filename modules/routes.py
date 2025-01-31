# modules/routes.py
from flask import Blueprint, render_template, session

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    user = session.get('user')
    return render_template('index.html', title="Secure Web Application", current_route="index", user=user)

@bp.route('/about')
def about():
    user = session.get('user')
    return render_template('about.html', title="About", current_route="about", user=user)

@bp.route('/contact')
def contact():
    user = session.get('user')
    return render_template('contact.html', title="Contact", current_route="contact", user=user)


@bp.route('/attacks')
def attacks():
    user = session.get('user')
    return render_template('attacks.html', title="Attacks", current_route="attacks", user=user)