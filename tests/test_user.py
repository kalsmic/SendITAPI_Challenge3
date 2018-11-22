# tests/test_register.py
from flask import json

user_with_missing_data = {
    "username": "",
    "firstname": "Arthur",
    "lastname": "kalule",
    "email": "kalulearthur@gmail.com",
    "password": "password",

}
user_with_complete_data = {
    "username": "user2",
    "firstname": "user2Fname",
    "lastname": "user2Lname",
    "email": "user2@gmail.com",
    "password": "user1"

}
user_input_wrong_dictionary_key = {
    "usernam": "user2",
    "firstname": "user2Fname",
    "lastname": "user2Lname",
    "email": "user2@gmail.com",
    "password": "password"

}
user_with_invalid_email_data = {
    "username": "john",
    "firstname": "Jonathan",
    "lastname": "Davis",
    "email": "jhdfdfmail.com",
    "password": "passswrd",
}


def test_user_registration(test_client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    # Tests register a user with missing data
    with test_client.post('/api/v2/auth/register', data=json.dumps(user_with_missing_data), headers=headers) as \
            create_user_with_missing_data:
        assert create_user_with_missing_data.status_code == 400
        data = json.loads(create_user_with_missing_data.data.decode())
        assert data == {"Message": "username cannot be empty"}

    # Tests register a user with wrong email
    with test_client.post('/api/v2/auth/register', data=json.dumps(user_with_invalid_email_data), headers=headers) as \
            create_user_with_wrong_email:
        assert create_user_with_wrong_email.status_code == 400
        data = json.loads(create_user_with_wrong_email.data.decode())
        assert data == {"Message": "Invalid email"}
    #
    # Test register  valid credentials
    with test_client.post('/api/v2/auth/register', data=json.dumps(user_with_complete_data), headers=headers) as \
            create_user_with_complete_data:
        assert create_user_with_complete_data.status_code == 200
        data = json.loads(create_user_with_complete_data.data.decode())
        assert data == {"success": "Registered Succesfully "}

    with test_client.post('/api/v2/auth/register', data=json.dumps(user_input_wrong_dictionary_key),
                          headers=headers) as register_user_with_bad_format_request:
        assert register_user_with_bad_format_request.status_code == 422


def test_user_login_(test_client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    # Tests login a user with wrong credentials
    with test_client.post('/api/v2/auth/login', data=json.dumps({"username": "admin", "password": "ajmin"}),
                          headers=headers) as  login_user_with_wrong_credentials:
        assert login_user_with_wrong_credentials.status_code == 400

    with test_client.post('/api/v2/auth/login', data=json.dumps({"username": "admin", "password": "admin"}),
                          headers=headers) as login_admin_user_with_correct_credentials:
        assert login_admin_user_with_correct_credentials.status_code == 200

    with test_client.post('/api/v2/auth/login', data=json.dumps({"username": "user1", "password": "user1"}),
                          headers=headers) as login_non_admin_user_with_correct_credentials:
        assert login_non_admin_user_with_correct_credentials.status_code == 200

    with test_client.post('/api/v2/auth/login', data=json.dumps({"usrname": "user2", "password": "password"}),
                          headers=headers) as login_non_admin_user_with_correct_credentials:
        assert login_non_admin_user_with_correct_credentials.status_code == 422