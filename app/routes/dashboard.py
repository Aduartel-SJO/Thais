from flask import Blueprint, render_template, redirect, url_for, session

dashboard_bp = Blueprint('dashboard', __name__, template_folder='../templates/')

@dashboard_bp.route('/')
def mesas():
    return render_template('mesas.html')