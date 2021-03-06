"""Views for the the admin Resource"""
from flask_restful import Resource, reqparse
from flask import request, Blueprint, jsonify, Flask
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
app = Flask(__name__)
from app.api.users.models import Admin

auth_blueprint = Blueprint('auth', __name__)

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('email', help="You must supply your email", required='False')
parser.add_argument('password', help="You must supply your no", required='True')

class LoginAdmin(Resource):
    """logs in the administrator"""
    def post(self):
        return Admin().login_admin(
            request.json['email'],
            request.json['password'])