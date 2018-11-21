# from flask import json
# from flask_jwt_extended import (
# create_access_token,
# get_jwt_identity
# )
#
# def generate_access_token(test_client):
#     # Tests register a user with correct credentials
#
#
#     token_data= test_client.post('/api/v2/auth/login',content_type="application/json",
#                           data=json.dumps({"username": "admin","password": "admin"}) )
#     return json.loads(token_data.data.decode())['access_token']
#
#
# def test_get_parcels(test_login_client):
#     mimetype = 'application/json'
#
#     headers = {
#         'Content-Type': mimetype,
#         'Accept': mimetype,
#         'Authorization': 'Bearer '+ generate_access_token()
#     }
#     with test_login_client.get('/api/v1/parcels',headers=headers) as response:
#         assert response.status_code == 200
#         data = json.loads(response.data.decode())
#         assert isinstance(data, dict)
#
#         # Parcels are list of dictionaries
#         assert isinstance(data['parcels'], list)
#
#         # A single parcel is of Type dictionary
#         assert isinstance(data['parcels'][0], dict)