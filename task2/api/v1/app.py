#!/usr/bin/env python3
"""
Entry point for the REST API
"""
from os import getenv
from flask import Flask, jsonify
from flask_cors import CORS
from api.v1.views import app_views
from api.models import init_db
from uuid import uuid4

app = Flask(__name__)
app.config['SECRET_KEY'] = getenv('ADN_SECRET_KEY', 'foobar')
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
CORS_ORIGIN_ALLOW_ALL = True
init_db()


@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": error.description}), 400


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({"message": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error):
    return jsonify({"message": "Forbidden"}), 403


@app.errorhandler(404)
def not_found(error):
    return jsonify({"message": "Not found"}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({"message": "Server error"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
