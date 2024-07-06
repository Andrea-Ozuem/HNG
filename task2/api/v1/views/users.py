#!/usr/bin/python3
'''
    RESTful API actions for auth actions
'''
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify, abort, request
#from api import db
from api.models.models import User, Organisation
from api.v1.views import app_views


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_userRec(user_id):
    'Gets user record associated with user id'
    jwt_id = get_jwt_identity()
    current_user = User.query.get(current_user)

    if current_user.id == user_id:
        return jsonify({
            "status": "success",
            "message": "User record retrieved successfully",
            "data": {
                "userId": current_user.id,
                "firstName": current_user.first_name,
                "lastName": current_user.last_name,
                "email": current_user.email,
                "phone": current_user.phone
            }
        }), 200
    else:
        

    # implement record of user in the org they belong to
    current_user.user_orgs.query
    return jsonify({}), 200

@app_views.route('/organisations', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_userOrg():
    'get orgs'
    jwt_id = get_jwt_identity()
    current_user = User.query.get(current_user)
    current_user.user_orgs

