# users.py
"""File contains routes for user end point"""

import re

from flask import (
    Blueprint,
    jsonify,
    request,
    json
)

from app.models.user import User

users_bp = Blueprint('users_bp', __name__, url_prefix='/api/v2')


@users_bp.route('/auth/register', methods=['POST'])
def register():
    """Expects Parameters:
            username(type - string)
            first_name(type - string)
            last_name(type - string)
            email(type - string)# NOTE:
            password(type - string)
    """
    data = request.data
    new_user = json.loads(data)

    # empty_fields = []

    # Traverse through the new_user input data
    for key, value in new_user.items():
        # check if field is empty
        if not value:
            return jsonify({'Message': "{} cannot be empty".format(key)}), 400


    if not re.match('[^@]+@[^@]+\.[^@]+', new_user['email']):
        return jsonify({'Message': "Invalid email"}), 400



    # validate email - to be worked on
    # if not validate_email(new_user['email']):
    #     return jsonify({"Message": "Please provide a valid email"}), 400

    # Submit valid data
    return User().sign_up(username=new_user['username'],
                          firstname=new_user['firstname'],
                          lastname=new_user['lastname'],
                          email=new_user['email'],
                          password=new_user['password']
                          )

