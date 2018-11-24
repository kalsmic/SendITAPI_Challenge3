from functools import wraps

from flask import jsonify
from flask_jwt_extended import (
    verify_jwt_in_request,
    get_jwt_identity
)

from .models.database import Database


def get_current_user_id():
    verify_jwt_in_request(),
    user_id = get_jwt_identity()
    return user_id['user_id']


def is_admin():
    """checks if logged in user is admin
    Returns True if True,False if False"""
    db = Database()
    db.cursor.execute("""SELECT is_admin FROM users WHERE user_id = {}""".format(get_current_user_id()))
    return db.cursor.fetchone()['is_admin']


def admin_required(func):
    """Restricts access to resources to admin users only"""

    @wraps(func)
    def wrapped(*args, **kwargs):
        if is_admin():
            return func(*args, **kwargs)
        return jsonify({"message": "You are not authorized to access this Resource"}), 401

    return wrapped


def non_admin_required(func):
    """Restricts access to resources to non admin users only"""

    @wraps(func)
    def wrapped(*args, **kwargs):
        if not is_admin():
            return func(*args, **kwargs)
        return jsonify({"message": "You are not authorized to access this Resource"}), 401

    return wrapped


limit_access_to_resource_owner = {"message": "You can only access resources that belong to you!"}


def cast_to_int(resource_id):
    # cast parcelId to int
    try:
        resource_id = int(resource_id)
    #     if id is not an integer
    except ValueError:
        return jsonify({"message": "Bad Request"}), 400


def parcel_does_not_exist():
    return jsonify({'message': 'Parcel does not exist'}), 400
