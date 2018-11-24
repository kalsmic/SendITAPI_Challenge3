# users.py
"""File contains routes for user end point"""

import re
from functools import wraps

from flask import (
    Blueprint,
    jsonify,
    request,
    json
)
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    verify_jwt_in_request,
    jwt_required
)

from app.models.user import User

users_bp = Blueprint('users_bp', __name__, url_prefix='/api/v2')

user_obj = User()

@users_bp.route('/auth/register', methods=['POST'])
def register():
    """Expects Parameters:
            username(type - string)
            first_name(type - string)
            last_name(type - string)
            email(type - string)
            password(type - string)
    """
    if not request.data:
        return jsonify({'Message': "Bad format request"}), 400

    new_user = json.loads(request.data)

    # Traverse through the new_user input data
    for key, value in new_user.items():
        # check if field is empty
        if not value:
            return jsonify({'Message': "{} cannot be empty".format(key)}), 400

        if isinstance(value,int):
            return jsonify({'Message': "{} cannot be a number".format(key)}), 400



    try:
        username = new_user['username']
        firstname = new_user['firstname']
        lastname = new_user['lastname']
        email = new_user['email']
        password = new_user['password']
    except KeyError:
        return jsonify({"message": "Bad format input"}), 422

    if not re.match('[^@]+@[^@]+\.[^@]+', new_user['email']):
        return jsonify({'Message': "Invalid email"}), 400

    # Submit valid data
    return User().sign_up(username=username, firstname=firstname, lastname=lastname, email=email, password=password)


@users_bp.route('/auth/login', methods=['POST'])
def login():
    """Expects Parameters:
            username(type - string)
            password(type - string)
    """

    if not request.data:
        return jsonify({'Message': "Bad format request"}), 400

    credentials = json.loads(request.data)

    # Traverse through the new_user input data
    for key, value in credentials.items():
        # check if field is empty
        if not value:
            return jsonify({'Message': "{} cannot be empty".format(key)}), 400

    try:
        username = credentials['username']
        password = credentials['password']
    except KeyError:
        return jsonify({"message": "Bad format input"}), 422

    # Submit valid data
    verify_user = user_obj.login_user(username=username, password=password)
    if verify_user['status'] == 'success':
        # create access token
        payload = {'user_id': verify_user['user_id']}

        access_token = create_access_token(identity=payload)

        return jsonify({"access_token": access_token}), 200
    # wrong user name or password
    return jsonify({"message": "Invalid credentials"}), 401


@users_bp.route('/<userId>/parcels', methods=['GET'])
@jwt_required
def get_a_parcel_by_userId(userId):
    """Fetch all parcel delivery
    orders by a specific user """

    # cast parcelId to int
    try:

        userId = int(userId)

    except ValueError:
        # userId is not a number
        # Therefore cannot be cast to an integer

        return jsonify({"message": "Bad Request"}), 400

    return user_obj.get_all_parcels_for_a_specific_user(userId)
