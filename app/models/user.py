import random
import string

from flask import jsonify
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
from flask_jwt_extended import get_jwt_identity,verify_jwt_in_request

from .database import Database



def get_current_user_id():
    verify_jwt_in_request(),
    user_id = get_jwt_identity()
    return user_id['user_id']

class User:
    role = 'user'

    def __init__(self):
        # create a database connection
        self.connect = Database()

    def sign_up(self, username, firstname, lastname, email, password, is_admin):
        self.connect.cursor.execute("SELECT * from users where username='{}'".format(username))

        if self.connect.cursor.fetchone():
            return jsonify({"Error": "Username Exists"})

        password = generate_password_hash(password, method='sha256')
        self.connect.cursor.execute("""INSERT INTO users (username,firstname,lastname,email,password,is_admin) 
        VALUES ( '{}','{}','{}','{}','{}','{}')""".format(username, firstname, lastname, email, password, is_admin))

        return jsonify({"success": 'Registered Succesfully '})

    def login_user(self, username, password):
        # self.connect.cur.execute("SELECT userId,username,password,is_admin FROM users where username='{}'"
        #                          .format(username))
        self.connect.cursor.execute("SELECT * FROM users where username='{}'"
                                 .format(username))

        user = self.connect.cursor.fetchone()
        # If username exists and has provided a valid password
        if user and check_password_hash(user['password'], password):
            return {'status': 'success', "is_admin": user['is_admin'], 'user_id': user['user_id']}
        return {'status': 'Failed'}



    def get_all_parcels_for_a_specific_user(self,userId):
        "Gets parcels for a specific user"
        owner_id = get_current_user_id()

        # query to get role of user
        self.connect.cursor.execute("SELECT is_admin FROM users where user_id={}".format(owner_id))

        is_admin = self.connect.cursor.fetchone()

        if is_admin['is_admin']:
            # if user is admin
            self.connect.cursor.execute("SELECT * from parcels where owner_id='{}'".format(userId))
            parcels = self.connect.cursor.fetchall()

            return jsonify({"parcels": parcels}), 200

        if not is_admin['is_admin'] and owner_id != userId:
            return jsonify({"message": "You can only access your parcel's"}),403

        self.connect.cursor.execute("SELECT * from parcels where owner_id='{}' AND owner_id='{}'".format(userId,owner_id))

        parcels=self.connect.cursor.fetchall()
        if parcels:
            return jsonify({"parcels":parcels}),200
        return jsonify({"message":"No parcels place yet"}),404





