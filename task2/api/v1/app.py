#!/usr/bin/env python3
"""
Entry point for the REST API
"""
from flask_cors import CORS
from api import create_app, db
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from api.v1.views import auth_views
from api.v1.views import app_views

app = create_app()
CORS(app, resources={"*": {"origins": "*"}})

app.config["JWT_SECRET_KEY"] = "super-secret"  # change using os.getenv!
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600
jwt = JWTManager(app)
app.register_blueprint(app_views)
app.register_blueprint(auth_views)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
