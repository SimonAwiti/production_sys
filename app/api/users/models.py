"""handles all operations for creating and fetching data relating to users"""
import psycopg2
from flask import request, jsonify, make_response, json
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash

from app.db import connections

class Helper():
    """Carries out common functions"""

    def check_if_user_exists(self, email):
        """
        Helper function to check if a user exists
        Returns a message if a user already exists
        """
        try:
            connect = connections.dbconnection()
            cursor = connect.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT * FROM admin WHERE email = '{}'".format(email))
            connect.commit()
            phone = cursor.fetchone()
            cursor.close()
            connect.close()
            if phone:
                return True
        except (Exception, psycopg2.DatabaseError) as error:
            return {'error' : '{}'.format(error)}, 401

class Admin(Helper):
    """Class to login admin"""
    def login_admin(self, email, password):
        """Logs in a user"""


        email = request.json.get('email', None)
        password = request.json.get('password', None)

        # Check for empty inputs
        if email == '' or password == '':
            return{
                "status": 401,
                "error": "Neither of the fields can be left empty during log in"
                }, 401

        try:
            get_user = "SELECT name, email, phone, password, isadmin, user_id \
                        FROM admin \
                        WHERE email = '" + email + "'" 
            connect = connections.dbconnection()
            cursor = connect.cursor(cursor_factory=RealDictCursor)
            cursor.execute(get_user)
            row = cursor.fetchone()
            if row is not None:
                access_token = create_access_token(identity=dict(name=row["name"], email=row['email'], phone=row['phone'], user_id=row["user_id"]))
                valid = check_password_hash(row.get('password'), password)
                if valid:
                    response = jsonify({
                        "user":{
                            'email':row['email'],
                            'phone':row['phone'],
                            'name':row['name']
                            },
                        "success":"Administrator Successfully logged in", 
                        "access_token":access_token})
                    response.status_code = 200
                    return response
            response = jsonify({"status": 401,
                "msg" : "Error logging in, credentials not found"})
            response.status_code = 401
            return response
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            response = jsonify({'status': 500,
                                'msg':'Problem fetching record from the database'})
            response.status_code = 500
            return response