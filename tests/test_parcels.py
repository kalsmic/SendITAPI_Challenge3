from flask_jwt_extended import create_access_token


def generate_header_with_token(role):
    if role == "admin":
        payload = {'user_id': 1}
    elif role == 'user':
        payload = {'user_id': 2}
    admin_token = create_access_token(identity=payload)
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Authorization': 'Bearer ' + admin_token
    }

    return headers


def test_admin_can_get_all_parcels_in_the_application(test_client):
    """Only admin can get all parcels in the application"""

    admin_gets_all_parcels = test_client.get('/api/v2/parcels', headers=generate_header_with_token('admin'))
    assert admin_gets_all_parcels.status_code == 200

    # user is not authorized to get all parcels in the application
    user_tries_to_gets_all_parcels =  test_client.get('/api/v2/parcels', headers=generate_header_with_token('user'))
    assert user_tries_to_gets_all_parcels.status_code == 401
