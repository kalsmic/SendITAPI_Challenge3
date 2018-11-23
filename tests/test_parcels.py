from flask import json
from flask_jwt_extended import create_access_token

missing_data = {
    "source_address": "",
    "destination_address": "d",
    "Item": "fe"
}
complete_data = {
    "source_address": "Jinja",
    "destination_address": "Mukono",
    "Item": "Text Books",

}
missing_data_response = {
    "message": "source_address cannot be empty"
}


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
    assert isinstance(json.loads(admin_gets_all_parcels.data.decode()), dict)
    assert isinstance(json.loads(admin_gets_all_parcels.data.decode())['parcels'], list)
    assert len(json.loads(admin_gets_all_parcels.data.decode())['parcels']) == 4

    # # user is not authorized to get all parcels in the application
    user_tries_to_gets_all_parcels =  test_client.get('/api/v2/parcels', headers=generate_header_with_token('user'))
    assert user_tries_to_gets_all_parcels.status_code == 401
    assert json.loads(user_tries_to_gets_all_parcels.data.decode()) == {"message":"You are not authorized to access this Resource"}

#
def test_get_cancel_a_parcel_with_invalid_parcel_id(test_client):
    # parcelId is an integer but does not exit
    with test_client.put('/api/v2/parcels/78/cancel',headers=generate_header_with_token('user')) as parcelId_out_of_bounds:
        "When id  is of type int but does not exist in the parcels" \
        "Then system returns an HTTP Error code of 400"""
        assert parcelId_out_of_bounds.status_code == 400
        assert json.loads(parcelId_out_of_bounds.data.decode()) == {'message': 'Parcel does not exist'}
#
#     # parcelId is not off type integer
    with test_client.put('/api/v2/parcels/7uf/cancel',headers=generate_header_with_token('user')) as parcelId_not_an_integer:
        """When an id that is not of type int is provided
        Then system returns an HTTP Error code of 400"""
        assert parcelId_not_an_integer.status_code == 400
        assert parcelId_not_an_integer.status_code == 400


def test_cancel_a_parcel_delivery_order_with_valid_parcelId(test_client):
    """Tests diffent Scenarios when Id is valid against the parcel's status"""
    # Pending
    with test_client.put('/api/v2/parcels/1/cancel',headers=generate_header_with_token('user')) as status_pending:
        """When parcel has a status of pending
        Then asset is modified
        And System returns its details are returned
         """
        assert status_pending.status_code == 200
        assert json.loads(status_pending.data.decode()) ==  {'message': {'destination_address': 'hoima',
                                                                         'item': 'HMIS Forms',
                                                                         'owner_id': 2,
                                                                         'parcel_id': 1,
                                                                         'present_location': 'Hoima',
                                                                         'source_address': 'Kotido',
                                                                         'status': 'cancelled'},
                                                                          'message': 'success'
                                                             }



#
#
#     #         In transit
#     with test_client.put('/api/v2/parcels/3/cancel',headers=generate_header_with_token('user')) as status_in_transit:
#         """When parcel has a status of In Transit
#         Then asset is not modified"""
#         assert status_in_transit.status_code == 400
#
#     #          Delivered
#     with test_client.put('/api/v2/parcels/4/cancel',headers=generate_header_with_token('user')) as status_delivered:
#         """When parcel has a status of Delivered
#              Then asset is not modified"""
#         assert status_delivered.status_code == 400
#
#
# def test_get_parcels_for_a_user_with_invalid_user_id(test_client):
#     # """ Given an API Consumer
#     # When I submit a GET request to /users/<userId>/parcels
#     # And no parcel orders exist for the given user id
#     # Then the system returns an HTTP status code of 404
#     # And a JSON representation of the error 'Not found' """
#
#     with test_client.get('/api/v2/users/er9/parcels',headers=generate_header_with_token('user')) as userId_Type_Error:
#         assert userId_Type_Error.status_code == 404
#
#     with test_client.get('/api/v2/users/9/parcels',headers=generate_header_with_token('user')) as userId_does_not_exist:
#         assert userId_does_not_exist.status_code == 404
#
#
# def test_get_parcels_for_a_valid_user_who_has_no_orders(test_client):
#     """When no orders exist for the specified userId"""
#     response = test_client.get('/api/v2/users/3/parcels',headers=generate_header_with_token('user'))
#     assert response.status_code == 404
#
#
# def test_create_a_parcel_delivery(test_client):
#     mimetype = 'application/json'
#     headers = {
#         'Content-Type': mimetype,
#         'Accept': mimetype
#     }
#
#     with test_client.post('/api/v2/parcels', data=json.dumps(missing_data),headers=generate_header_with_token('user')) as \
#             create_order_with_missing_data:
#         assert create_order_with_missing_data.content_type == mimetype
#         assert create_order_with_missing_data.status_code == 400
#
#     with test_client.post('/api/v2/parcels', data=json.dumps(complete_data), headers=generate_header_with_token('user')) as \
#             create_order_with_complete_data:
#         assert create_order_with_complete_data.content_type == mimetype
#         assert create_order_with_complete_data.status_code == 422
#         assert json.loads(create_order_with_complete_data.data.decode()) ==  {'message': 'Bad format input'}
#
#
#
# #
# # def test_get_a_parcel_with_invalid_parcel_id(test_client):
# #     """When an invalid parcel Id is provided"""
# #
# #     with test_client.get('/api/v2/parcels/0',headers=generate_header_with_token('user')) as parcelId_out_of_bounds:
# #         """Id is a number and does not exist in the parcels
# #            Then system returns the specific parcel and a status code of 400"""
# #         assert parcelId_out_of_bounds.status_code == 400
# #
# #     with test_client.get('/api/v2/parcels/7uf',headers=generate_header_with_token('user')) as parcelId_not_an_integer:
# #         """parcelId is not a number
# #                    Then system returns the specific parcel and a status code of 400"""
# #         assert parcelId_not_an_integer.status_code == 400
# #
# #
# # def test_get_a_parcel_with_parcelId_which_exists_and_is_valid(test_client):
# #     """Given a valid parcel Id
# #         Then system returns the specific parcel and a status code of 200"""
# #     response = test_client.get('/api/v2/parcels/1',headers=generate_header_with_token('user'))
# #     assert response.status_code == 400
# #
# # def test_get_user_updates_status_of_a_parcel(test_client):
# #     """Given a valid parcel Id
# #         Then system returns the specific parcel and a status code of 200"""
# #     response = test_client.get('/api/v2/parcels/1/status',headers=generate_header_with_token('user'))
# #     assert response.status_code == 405
# #     assert json.loads(response.data.decode()) == {"message": "You are not authorized to access this Resource"}
