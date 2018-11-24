from flask import json
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


def test_gets_all_parcels_in_the_application(test_client):
    """Tests get all parcel delivery orders in the application"""

    with test_client.get('/api/v2/parcels', headers=generate_header_with_token(1)) as admin_gets_all_parcels:
        """Admin gets all parcels in the application"""

        assert admin_gets_all_parcels.status_code == 200
        assert isinstance(json.loads(admin_gets_all_parcels.data.decode()), dict)
        assert isinstance(json.loads(admin_gets_all_parcels.data.decode())['parcels'], list)
        assert len(json.loads(admin_gets_all_parcels.data.decode())['parcels']) == 4

    with test_client.get('/api/v2/parcels', headers=generate_header_with_token(2)) as \
            user_should_not_gets_all_parcels_in_the_application:
        """User cannot access this route"""

        assert user_should_not_gets_all_parcels_in_the_application.status_code == 401
        assert json.loads(user_should_not_gets_all_parcels_in_the_application.data.decode()) == \
               {"message": "You are not authorized to access this Resource"}

    # # user is not authorized to get all parcels in the application
    user_tries_to_gets_all_parcels = test_client.get('/api/v2/parcels', headers=generate_header_with_token(2))
    assert user_tries_to_gets_all_parcels.status_code == 401
    assert json.loads(user_tries_to_gets_all_parcels.data.decode()) == {
        "message": "You are not authorized to access this Resource"}


#
def test_get_cancel_a_parcel_with_invalid_parcel_id(test_client):
    # parcelId is an integer but does not exit
    with test_client.put('/api/v2/parcels/78/cancel', headers=generate_header_with_token(2)) as parcelId_out_of_bounds:
        "When id  is of type int but does not exist in the parcels" \
        "Then system returns an HTTP Error code of 400"""
        assert parcelId_out_of_bounds.status_code == 400
        assert json.loads(parcelId_out_of_bounds.data.decode()) == {'message': 'Parcel does not exist'}
    #
    #     # parcelId is not off type integer
    with test_client.put('/api/v2/parcels/7uf/cancel',
                         headers=generate_header_with_token(2)) as parcelId_not_an_integer:
        """When an id that is not of type int is provided
        Then system returns an HTTP Error code of 400"""
        assert parcelId_not_an_integer.status_code == 400
        assert json.loads(parcelId_not_an_integer.data.decode()) == {"message": "Bad Request"}


def test_cancel_a_parcel_delivery_order_with_valid_parcelId(test_client):
    """Tests diffent Scenarios when Id is valid against the parcel's status"""

    with test_client.put('/api/v2/parcels/98/cancel', headers=generate_header_with_token(2)) as \
            user_cancels_parcel_which_does_not_exist:
        """When user tries to cancel a parcel that does not belong to them """
        assert user_cancels_parcel_which_does_not_exist.status_code == 400
        assert json.loads(user_cancels_parcel_which_does_not_exist.data.decode()) == \
               {"message": "Parcel does not exist"}

    with test_client.put('/api/v2/parcels/1/cancel', headers=generate_header_with_token(3)) as \
            user_cancels_parcel_for_another_user:
        """When user tries to cancel a parcel that does not belong to them """
        assert user_cancels_parcel_for_another_user.status_code == 405
        assert json.loads(user_cancels_parcel_for_another_user.data.decode()) == \
               {"message": "You're not allowed to perform this action"}

    with test_client.put('/api/v2/parcels/3/cancel', headers=generate_header_with_token(2)) as \
            user_cancels_parcel_which_is_not_pending:
        """When user tries to cancel a parcel which is not pending """
        assert user_cancels_parcel_which_is_not_pending.status_code == 403
        assert json.loads(user_cancels_parcel_which_is_not_pending.data.decode()) == \
               {"message": "Cannot cancel a parcel which is already delivered"}

        # Pending
    with test_client.put('/api/v2/parcels/1/cancel', headers=generate_header_with_token(2)) as status_pending:
        """When parcel has a status of pending
        Then asset is modified
        And System returns its details are returned
         """
        assert status_pending.status_code == 200
        assert json.loads(status_pending.data) == {'parcel': {'destination_address': 'hoima',
                                                              'item': 'HMIS Forms',
                                                              'owner_id': 2,
                                                              'parcel_id': 1,
                                                              'present_location': 'Hoima',
                                                              'source_address': 'Kotido',
                                                              'status': 'cancelled'},
                                                   'message': 'success'
                                                   }


def test_get_a_parcel_delivery_order(test_client):
    """Tests scenarios for get a specific delivery order endpoint"""

    with test_client.get('/api/v2/parcels/dfd',
                         headers=generate_header_with_token(1)) as get_parcel_with_non_numeric_parcel_id:
        """When a non numeric is provided as a parameter,
        The system returns a 400 HTTP status code 
        And an error message 'Provide a valid parcel Id'"""

        assert get_parcel_with_non_numeric_parcel_id.status_code == 400
        assert json.loads(get_parcel_with_non_numeric_parcel_id.data.decode()) == {
            "message": "Provide a valid parcel Id"}

    with test_client.get('/api/v2/parcels/93', headers=generate_header_with_token(2)) as \
            user_gets_a_parcels_with_a_parcel_id_which_does_not_exist:
        """When a non numeric is provided as a parameter,
        The system returns a 400 HTTP status code 
        And an error message 'Provide a valid parcel Id'"""

        assert user_gets_a_parcels_with_a_parcel_id_which_does_not_exist.status_code == 400
        assert json.loads(user_gets_a_parcels_with_a_parcel_id_which_does_not_exist.data.decode()) == \
               {'message': 'Parcel does not exist'}

    with test_client.get('/api/v2/parcels/1', headers=generate_header_with_token(3)) as \
            non_admin_user_gets_a_parcels_which_does_not_belong_to_them:
        """When a non admin user sends a request to get a parcel which does not belong to them,
        The system returns a 403 HTTP status code 
        And an error message 'You can only access resources that belong to you'"""

        assert non_admin_user_gets_a_parcels_which_does_not_belong_to_them.status_code == 403
        assert json.loads(non_admin_user_gets_a_parcels_which_does_not_belong_to_them.data.decode()) == \
               {"message": "You can only access resources that belong to you!"}

    with test_client.get('/api/v2/parcels/4', headers=generate_header_with_token(3)) as \
            non_admin_user_gets_a_parcels_which_exists_and_belongs_to_them:
        """When a non admin user sends a request to get a parcel which exists and belongs to them,
        The system returns a 200 HTTP status code
        And the details of the parcel for the specified parcel Id'"""

        assert non_admin_user_gets_a_parcels_which_exists_and_belongs_to_them.status_code == 200
        assert json.loads(non_admin_user_gets_a_parcels_which_exists_and_belongs_to_them.data.decode()) == \
               {'parcel': {'destination_address': 'Ntinda',
                           'item': 'Text Books',
                           'present_location': 'Naalya',
                           'source_address': 'Naalya',
                           'status': 'cancelled',
                           'user_id': 3,
                           'username': 'user2'},
                'status': 'success'}

        with test_client.get('/api/v2/parcels/4', headers=generate_header_with_token(1)) as \
                admin_user_gets_a_parcels_which_exists:
            """When a non admin user sends a request to get a parcel which does not belong to them,
            The system returns a 200 HTTP status code
            And an the details of the parcel for the specified Parcel Id'"""

            assert admin_user_gets_a_parcels_which_exists.status_code == 200
            assert json.loads(admin_user_gets_a_parcels_which_exists.data.decode()) == \
                   {'parcel': {'destination_address': 'Ntinda',
                               'item': 'Text Books',
                               'present_location': 'Naalya',
                               'source_address': 'Naalya',
                               'status': 'cancelled',
                               'user_id': 3,
                               'username': 'user2'},
                    'status': 'success'}


def test_create_a_parcel_delivery_order(test_client):
    """Tests for the different scenarios of user creating a parcel delivery order"""

    with test_client.post('/api/v2/parcels', headers=generate_header_with_token(1),
                          data=json.dumps(complete_new_parcel_data)) as admin_creates_a_parcel_delivery_order:
        """When admin user sends a post request to create a parcel delivery order
           Then system does not create the parcel delivery order 
           And system returns an HTTP response with  
            - a status code of 1
            - and a message 'You are not authorized to access this Resource
        """
        assert admin_creates_a_parcel_delivery_order.status_code == 401
        assert json.loads(admin_creates_a_parcel_delivery_order.data.decode()) ==\
               {"message": "You are not authorized to access this Resource"}
