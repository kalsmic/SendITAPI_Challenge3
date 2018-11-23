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

def test_get_all_parcels_for_a_specific_user(test_client):
    """Only admin can get all parcels in the application"""

    # user does not exist
    response1 = test_client.get('/api/v2/87/parcels', headers=generate_header_with_token('user'))
    assert response1.status_code == 403

    #uparcels belong to another user
    response2 = test_client.get('/api/v2/1/parcels', headers=generate_header_with_token('user'))
    assert response2.status_code == 403

    # user id is invalid to another user
    response3 = test_client.get('/api/v2/gf/parcels', headers=generate_header_with_token('user'))
    assert response3.status_code == 400

    # user id is invalid to another user
    response3 = test_client.get('/api/v2/gf/parcels', headers=generate_header_with_token('user'))
    assert response3.status_code == 400

    #user gets their parcels
    response4 =  test_client.get('/api/v2/2/parcels', headers=generate_header_with_token('user'))
    assert response4.status_code == 404



