# parcels.py
"""This file contains routes for parcels"""

from flask import (
    Blueprint,
    jsonify,
    request,
    json
)
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request

from app.models.parcel import ParcelOrder
from app.views.users import admin_required, non_admin

parcels_bp = Blueprint('parcels_bp', __name__, url_prefix='/api/v2')
parcels_obj = ParcelOrder()


def get_current_user_id():
    verify_jwt_in_request(),
    user_id = get_jwt_identity()
    return user_id['user_id']


@parcels_bp.route('/parcels', methods=['GET'])
@jwt_required
@admin_required
def get_all_parcels():
    """Fetch all parcel delivery orders"""

    return jsonify({'parcels': parcels_obj.parcel_details()}), 200


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
        return jsonify({"message": "Bad Request"}), 400

    # Avoids returning the last item if parcel id of zero is given
    """checks if parcel id exists"""
    parcels_obj.connect.cursor.execute("SELECT * FROM parcels where parcel_id = '%s'", (parcelId,))

    # returns parcel with valid parcel id
    if parcels_obj.connect.cursor.rowcount > 0:
        parcel_order = parcels_obj.connect.cur.fetchone()

        return jsonify({'parcel': parcel_order}), 200
    return jsonify({'message': "Bad Requests"}), 400


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

    data = request.data
    parcelDict = json.loads(data)
    # Traverse through the input
    for key, value in parcelDict.items():

        # check if field is empty
        if not value:
            return jsonify({'message': "{} cannot be empty".format(key)}), 400

    # add new parcel order

    result = parcels_obj.insert__a_parcel(item=parcelDict['item'],
                                          pick_up_location=parcelDict['pick_up_location'],
                                          pick_up_date=parcelDict['pick_up_date'],
                                          destination=parcelDict['destination'],
                                          owner_id=get_current_user_id()
                                          )

    return jsonify({"parcel": 'Parcel Created Successfully'}), 201


@parcels_bp.route('/parcels/<parcelId>/cancel', methods=['PUT'])
@jwt_required
@non_admin
def cancel_a_delivery_order(parcelId):
    """Parameter: integer parcelId
       Returns: 400 if parcelId is not  of type int
       Returns: 200 if parcel's successfully cancelled and the details of the specific parcel
       Returns : 304 if parcel is Already cancelled or Delivered
    """
    # cast parcelId to int
    try:
        parcelId = int(parcelId)
    #     if parcel id is not an integer
    except ValueError:
        return jsonify({"message": "Bad Request"}), 400

    return parcels_obj.cancel_a_parcel(parcelId, 2, 'Cancelled')

