# tests/test_register.py
from flask import json
user_with_missing_data = {
    "username": "",
    "firstname": "Arhtur",
    "lastname": "kalule",
    "email": "kalulearthur@gmail.com",
    "password": "passswrd"

}
user_with_complete_data = {
    "username": "micheal",
    "firstname": "Arhtur",
    "lastname": "kalule",
    "email": "kalulearthur@gmail.com",
    "password": "passswrd"

}
user_with_wrong_email_data = {
    "username": "micheal",
    "firstname": "Arhtur",
    "lastname": "kalule",
    "email": "shjgmail.com",
    "password": "passswrd"

}



def test_register_user(test_client):
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
        assert data == { "message": "username cannot be empty"}

    # Tests register a user with wrong email
    with test_client.post('/api/v2/auth/register', data=json.dumps(user_with_wrong_email_data), headers=headers) as \
            create_user_with_wrong_email:
        assert create_user_with_wrong_email.status_code == 200
        data = json.loads(create_user_with_wrong_email.data.decode())
        assert data == {"success": "Registered Succesfully " }

    # Test register  valid credentials
    with test_client.post('/api/v2/auth/register', data=json.dumps(user_with_complete_data), headers=headers) as \
            create_user_with_complete_data:
        assert create_user_with_complete_data.status_code == 200
        data = json.loads(create_user_with_complete_data.data.decode())
        assert data == {"success": "Registered Succesfully "}
