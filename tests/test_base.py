# tests/test_base.py

"""Module contains input data for tests"""
from flask_jwt_extended import create_access_token

missing_data = {
    "source_address": "",
    "destination_address": "d",
    "Item": "fe"
}
complete_new_parcel_data = {
    "source_address": "Jinja",
    "destination_address": "Mukono",
    "Item": "Text Books",

}
new_parcel_data_with_wrong_key = {
    "source": "Jinja",
    "destination_address": "Mukono",
    "Item": "Text Books",

}
missing_data_response = {
    "message": "source_address cannot be empty"
}


def generate_header_with_token(id):
    admin_token = create_access_token(identity={'user_id': id})
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Authorization': 'Bearer ' + admin_token
    }

    return headers

