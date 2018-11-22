# parcels.py
"""This file contains routes for parcels"""

from flask import (
    Blueprint,
    jsonify,
    request,
    json
)
from flask_jwt_extended import jwt_required

from app.helpers import (
    get_current_user_id
)
from app.models.parcel import ParcelOrder
from app.views.users import admin_required, non_admin

parcels_bp = Blueprint('parcels_bp', __name__, url_prefix='/api/v2')
parcels_obj = ParcelOrder()


@parcels_bp.route('/parcels', methods=['GET'])
# @jwt_required
# @admin_required
def get_all_parcels():
    """Fetch all parcel delivery orders"""

    return jsonify({'parcels': parcels_obj.parcel_details()}), 200


#
@parcels_bp.route('/parcels/<parcelId>', methods=['GET'])
@jwt_required
@non_admin
def get_a_parcel(parcelId):
    """Parameter: int parcelId
    :returns:
        404 error If parcelId is not an integer or does not exist
        200 success if parcelId exists"""

    # cast parcelId to int
    try:
        parcelId = int(parcelId)
    #     if parcel id is not an integer
    except ValueError:
        return jsonify({"message": "Provide a valid parcel Id"}), 400

    # Avoids returning the last item if parcel id of zero is given
    """checks if parcel id exists"""
    parcels_obj.connect.cursor.execute("SELECT * FROM parcels where parcel_id = '%s'", (parcelId,))

    # returns parcel with valid parcel id
    if parcels_obj.connect.cursor.rowcount > 0:
        parcel_order = parcels_obj.connect.cur.fetchone()

        return jsonify({'parcel': parcel_order}), 200
    return jsonify({'message': "Parcel delivery order does not exist"}), 400


@parcels_bp.route('/parcels', methods=['POST'])
@jwt_required
@non_admin
def add_a_parcel_order():
    """Create a parcel delivery order
    Expects parameters:
        Item: type string
        pickUp: type string
        destination: type string
        ownerId: type int
    Returns:
        400 error code if required parameter is not provided
        201 HTTP error code  if Order is created Successfully

#     """

    # Check if request data is provided
    if not request.data:
        return jsonify({'Message': "Bad format request"}), 400

    parcelDict = json.loads(request.data)

    # Traverse through the input
    for key, value in parcelDict.items():

        # check if field is empty
        if not value:
            return jsonify({'message': "{} cannot be empty".format(key)}), 400

    # check if valid dictionary keys have been provided
    try:
        item = parcelDict['item']
        pick_up_location = parcelDict['pick_up_location']
        pick_up_date = parcelDict['pick_up_date']
        destination = parcelDict['destination']
    except KeyError:
        return jsonify({"message": "Bad format input"}), 422

    # add new parcel order

    result = parcels_obj.insert__a_parcel(item=item, pick_up_location=pick_up_location, pick_up_date=pick_up_date,
                                          destination=destination, owner_id=get_current_user_id())

    return jsonify({"parcel": 'Parcel Created Successfully'}), 201


@parcels_bp.route('/parcels/<parcelId>/cancel', methods=['PUT'])
@jwt_required
@non_admin
def cancel_a_delivery_order(parcelId):
    """Parameter: integer parcelId
       Returns: 400 if parcelId is not  of type int
       Returns: 200 if parcel's successfully cancelled
       Returns : 304 if parcel is Already cancelled or Delivered
    """
    # cast parcelId to int
    try:
        parcelId = int(parcelId)
    #     if parcel id is not an integer
    except ValueError:
        return jsonify({"message": "Bad Request"}), 400

    owner_id = get_current_user_id()

    return parcels_obj.cancel_a_parcel(parcelId, owner_id, 'Cancelled')


@parcels_bp.route('/parcels/<parcelId>/status', methods=['PUT'])
@jwt_required
@admin_required
def update_parcel_status(parcelId):
    """Parameter: integer parcelId
       Returns: 400 if parcelId is not  of type int
       Returns: 200 if parcel's status is successfully updated
    """
    # cast parcelId to int
    try:
        parcelId = int(parcelId)
    #     if parcel id is not an integer
    except ValueError:
        return jsonify({"message": "Bad Request"}), 400

    # check if request data is provided
    if not request.data:
        return jsonify({'Message': "Bad format request"}), 400

    new_parcel_status = json.loads(request.data)

    # check if valid dictionary keys have been provided
    try:
        new_parcel_status['parcelStatus']
    except KeyError:
        return jsonify({"message": "Bad format input"}), 422

    # Check if input data is empty
    if not new_parcel_status['parcelStatus']:
        return jsonify({"message": "parcel status cannot be empty"}), 400

    # Cannot update parcel status who's status is neither in transit or delivered
    if new_parcel_status['parcelStatus'] not in ['in transit', 'delivered']:
        return jsonify({"message": "Parcel's status Cannot be updated to " + new_parcel_status['parcelStatus']}), 400

    return parcels_obj.update_parcel_status(parcelId, new_parcel_status['parcelStatus'])


@parcels_bp.route('/parcels/<parcelId>/presentLocation', methods=['PUT'])
@jwt_required
@admin_required
def update_parcel_present_location(parcelId):
    """Parameter: integer parcelId
       Returns: 400 if parcelId is not  of type int
       Returns: 200 if parcel's status is successfully updated
    """
    # cast parcelId to int
    try:
        parcelId = int(parcelId)
    #     if parcel id is not an integer
    except ValueError:
        return jsonify({"message": "Bad Request"}), 400

    if not request.data:
        return jsonify({'Message': "Bad format request"}), 400

    new_parcel_present_location = json.loads(request.data)
    new_parcel_present_location = new_parcel_present_location['presentLocation']

    # Check if input data is empty
    if not new_parcel_present_location:
        return jsonify({"message": "parcel's new present location cannot be empty"}), 400

    # Check if new present location is an integer
    if isinstance(new_parcel_present_location, int):
        return jsonify({"message": "parcel's new present location cannot be an integer"}), 400

    return parcels_obj.update_parcel_present_location(parcelId=parcelId,
                                                      new_present_location=new_parcel_present_location)


@parcels_bp.route('/parcels/<parcelId>/destination', methods=['PUT'])
@jwt_required
@non_admin
def update_present_parcel_destination(parcelId):
    """Parameter: integer parcelId
       Returns: 400 if parcelId is not  of type int
       Returns: 200 if parcel's destination is successfully updated
    """
    # cast parcelId to int
    try:
        parcelId = int(parcelId)
    #     if parcel id is not an integer
    except ValueError:
        return jsonify({"message": "Bad Request"}), 400

    if not request.data:
        return jsonify({'Message': "Bad format request"}), 400

    new_present_parcel_destination = json.loads(request.data)

    # Check if data contains valid dictionary keys
    try:
        new_present_parcel_destination = new_present_parcel_destination['destinationAddress']
    except KeyError:
        return jsonify({"message": "Bad format input"}), 422

    # Check if input data is empty
    if not new_present_parcel_destination:
        return jsonify({"message": "parcel's new present location cannot be empty"}), 400

    # Check if new parcel destination location is an integer
    if isinstance(new_present_parcel_destination, int):
        return jsonify({"message": "parcel's destination cannot be an integer"}), 400

    return parcels_obj.update_parcel_destination_address(parcelId=parcelId,
                                                         new_destination_address=new_present_parcel_destination)
