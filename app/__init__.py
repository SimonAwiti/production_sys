# app/__init__.py
import os
from flask import Flask, redirect, jsonify,render_template, request, url_for
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import datetime, timedelta

#local import
from app.db.connections import initializedb
from app.api.users.models import Admin
#from instance.config import app_config


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True, static_url_path='/static')
    app.url_map.strict_slashes = False
    CORS(app)

  
    def configure_blueprints(app):
        """ Configure blueprints . """
        from app.routes.routes import auth_blueprint

        app_blueprints = [ auth_blueprint ]

        for bp in app_blueprints:
            CORS(bp)
            app.register_blueprint(bp)

    """register the blueprints"""
    configure_blueprints(app) 

 
    initializedb()
    app.config['JWT_SECRET_KEY'] = 'SECRET'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=100) 
    jwt = JWTManager(app)
    app.secret_key = "secret key"



    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/login",methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            login = Admin().login_admin(
                request.json['email'],
                request.json['password'])
            if Admin.status_code is 200:
                return redirect(url_for("index"))
        return render_template("login.html")
        

    return app
