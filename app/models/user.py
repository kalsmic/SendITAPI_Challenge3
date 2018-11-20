from flask import jsonify

from .database import Database
from  werkzeug.security import (
    generate_password_hash,
    check_password_hash
)




class User:
    role = 'user'

    def __init__(self):
        # create a database connection
        self.connect = Database()

    def sign_up(self, username, firstname, lastname, email, password):
        self.connect.cur.execute("SELECT * from users where username='{}'".format(username))

        if self.connect.cur.fetchone():
            return jsonify({"Error": "Username Exists"})

        password = generate_password_hash(password, method='sha256')
        self.connect.cur.execute("""INSERT INTO users (username,firstname,lastname,email,password) 
        VALUES ( '{}','{}','{}','{}','{}')""".format(username, firstname, lastname, email, password))

        return jsonify({"success": 'Registered Succesfully '})

    def login_user(self, username, password):
        self.connect.cur.execute("SELECT username,password FROM users where username='{}'"
                                 .format(username))

        user = self.connect.cur.fetchone()
        # If username exists
        if user:
        #     verify password
            if check_password_hash(user['password'],password):
                # password is correct
                return True
        # wrong username or password
        return False

