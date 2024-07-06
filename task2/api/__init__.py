#!/usr/bin/env python3

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres.mabofogfvkhsgtcgwndo:xender2022$@aws-0-eu-central-1.pooler.supabase.com:6543/postgres'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    #app.config['SECRET_KEY'] = getenv('ADN_SECRET_KEY', 'foobar')
    
    CORS(app, resources={"*": {"origins": "*"}})

    db.init_app(app)

    return app