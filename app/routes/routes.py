from flask import request, Blueprint, jsonify, Flask, render_template
app = Flask(__name__)

auth_blueprint = Blueprint('auth', __name__)

"""Importing endpoints"""
from app.api.users.views import LoginAdmin



"""Define the apis"""
admin_login = LoginAdmin.as_view('login_admin')


"""Issuing the actual URLS"""

"""admin login"""
auth_blueprint.add_url_rule(
    '/login/admin', 
    view_func=admin_login,
    methods=['POST'])

