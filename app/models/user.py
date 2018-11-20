from flask import jsonify
from werkzeug.security import generate_password_hash

from .database import Database


class User:
    role = 'user'

    def __init__(self):
        # create a database connection
        self.connect = Database.__init__(self)

    def sign_up(self, username, firstname, lastname, email, password):
        # SQL_check_user_exists = self.connect.execute("SELECT * from users where username = %s", (username,))
        SQL_check_user_exists = self.connect.execute("SELECT * from users where username='{}'".format(username))

        if self.connect.fetchone():
            return jsonify({"Error": "Username Exists"})

        password = generate_password_hash(password, method='sha256')
        SQL_insert_new_user = self.connect.execute("""INSERT INTO users (username,firstname,lastname,email,password) 
        VALUES ( %s,%s,%s,%s,%s)""", (username, firstname, lastname, email, password))

        return jsonify({"success": 'Registered Succesfully '})


