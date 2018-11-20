# tests/test_register.py
from flask import json
user_correct_credentials = {
    "username": "admin",
    "password": "admin"
}

user_wrong_credentials = {
    "username": "admin",
    "password": "passswrd"
}



def test_register_user(test_client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    # Tests register a user with missing data
    with test_client.post('/api/v2/auth/login', data=json.dumps(user_wrong_credentials), headers=headers) as \
            login_user_with_wrong_credentials:
        assert login_user_with_wrong_credentials.status_code == 400


    # Tests register a user with wrong email
    with test_client.post('/api/v2/auth/login', data=json.dumps(user_correct_credentials), headers=headers) as \
            login_user_with_correct_credentials:
        assert login_user_with_correct_credentials.status_code == 200

