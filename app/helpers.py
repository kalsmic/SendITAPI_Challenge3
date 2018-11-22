from flask_jwt_extended import (
verify_jwt_in_request,
get_jwt_identity
)

def get_current_user_id():
    verify_jwt_in_request(),
    user_id = get_jwt_identity()
    return user_id['user_id']

def cast_to_int(resource_id):
 # cast parcelId to int
    try:
        resource_id = int(resource_id)
    #     if id is not an integer
    except ValueError:
        return jsonify({"message": "Bad Request"}), 400



