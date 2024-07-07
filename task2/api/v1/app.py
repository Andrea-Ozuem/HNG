#!/usr/bin/env python3
"""
Entry point for the REST API
"""

from api.models.models import User, Organisation
from api import create_app, db
#from api.v1.views import app_views
from flask_jwt_extended import JWTManager
from api.v1.views import auth_views
from api.v1.views import app_views

app = create_app()
app.config["JWT_SECRET_KEY"] = "super-secret"  # change using os.getenv!
# app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
jwt = JWTManager(app)
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 3600,
    'connect_args': {'connect_timeout': 10}
}
app.register_blueprint(app_views)
app.register_blueprint(auth_views)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
