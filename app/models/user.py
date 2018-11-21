import random
import string

from flask import jsonify
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
from flask_jwt_extended import get_jwt_identity
from functools import wraps

from .database import Database

# generates an alpha numeric string of 32
secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))




class User:
    role = 'user'

    def __init__(self):
        # create a database connection
        self.connect = Database()

    def sign_up(self, username, firstname, lastname, email, password, is_admin):
        self.connect.cur.execute("SELECT * from users where username='{}'".format(username))

        if self.connect.cur.fetchone():
            return jsonify({"Error": "Username Exists"})

        password = generate_password_hash(password, method='sha256')
        self.connect.cur.execute("""INSERT INTO users (username,firstname,lastname,email,password,is_admin) 
        VALUES ( '{}','{}','{}','{}','{}','{}')""".format(username, firstname, lastname, email, password, is_admin))

        return jsonify({"success": 'Registered Succesfully '})

    def login_user(self, username, password):
        # self.connect.cur.execute("SELECT userId,username,password,is_admin FROM users where username='{}'"
        #                          .format(username))
        self.connect.cur.execute("SELECT * FROM users where username='{}'"
                                 .format(username))

        user = self.connect.cur.fetchone()
        # If username exists and has provided a valid password
        if user and check_password_hash(user['password'], password):
            return {'status': 'success', "is_admin": user['is_admin'], 'user_id': user['user_id']}
        return {'status': 'Failed'}


