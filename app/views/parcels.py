# parcels.py
"""This file contains routes for parcels"""

from flask import (
    Blueprint,
    jsonify
)
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.parcel import ParcelOrder
from app.views.users import admin_required

parcels_bp = Blueprint('parcels_bp', __name__, url_prefix='/api/v2')
parcels_obj = ParcelOrder()


@parcels_bp.route('/parcels', methods=['GET'])
@jwt_required
@admin_required
def get_all_parcels():
    """Fetch all parcel delivery orders"""

    return jsonify({'parcels': parcels_obj.parcel_details()}), 200

#
# @parcels_bp.route('/parcels/<parcelId>', methods=['GET'])
# def get_a_parcel(parcelId):
#     """Parameter: int parcelId
#     :returns:
#         404 error If parcelId is not an integer or does not exist
#         200 success if parcelId exists"""
#
#     # cast parcelId to int
#     try:
#         parcelId = int(parcelId)
#     #     if parcel id is not an integer
#     except ValueError:
#         return jsonify(Bad_request), 400
#
#     # Avoids returning the last item if parcel id of zero is given
#     """checks if parcel id exists"""
#     if parcelId not in parcel_id_table.keys():
#         return jsonify(Bad_request), 400
#
#     # returns parcel with valid parcel id
#     return jsonify({'parcel': parcelOrders[parcelId - 1].parcel_details()}), 200
#
#
# @parcels_bp.route('/parcels', methods=['POST'])
# def add_a_parcel_order():
#     """Create a parcel delivery order
#     Expects parameters:
#         Item: type string
#         pickUp: type string
#         destination: type string
#         ownerId: type int
#     Returns:
#         400 error code if required parameter is not provided
#         201 HTTP error code  if Order is created Successfully
#
# #     """
#
#     data = request.data
#     parcelDict = json.loads(data)
#
#     # check if userId is valid
#     if parcelDict['ownerId'] and not verify_user_id(parcelDict['ownerId']):
#         return jsonify(Bad_request), 400
#
#     # Traverse through the input
#     for key, value in parcelDict.items():
#
#         # check if field is empty
#         if not value:
#             return jsonify({'message': "{} cannot be empty".format(key)}), 400
#
#     # add new parcel order
#     newParcel = ParcelOrder(
#         parcelDict['Item'],
#         parcelDict['pickUp'],
#         parcelDict['destination'],
#         'Pending',
#         parcelDict['ownerId']
#     )
#     parcelOrders.append(newParcel)
#     # return new parcel with parcel it attached to it
#     return jsonify({'parcel': newParcel.parcel_details()}), 201
#
#
# @parcels_bp.route('/parcels/<parcelId>/cancel', methods=['PUT'])
# def cancel_a_delivery_order(parcelId):
#     """Parameter: integer parcelId
#        Returns: 400 if parcelId is not  of type int
#        Returns: 200 if parcel's successfully cancelled and the details of the specific parcel
#        Returns : 304 if parcel is Already cancelled or Delivered
#     """
#     # cast parcelId to int
#     try:
#         parcelId = int(parcelId)
#     #     if parcel id is not an integer
#     except ValueError:
#         return jsonify(Bad_request), 400
#
#     # Check if parcel id exists in the parcel's table
#     """checks if parcel id exists"""
#     if parcelId not in parcel_id_table.keys():
#         return jsonify(Bad_request), 400
#
#     # Check if parcel is still pending
#     if parcelOrders[parcelId - 1].status.upper() == 'PENDING':
#         parcelOrders[parcelId - 1].status = 'Cancelled'
#         return jsonify({'parcel': parcelOrders[parcelId - 1].parcel_details()}), 200
#
#     # Cannot cancel parcels with status cancelled, In transit or delivered
#     return jsonify(Not_modified), 304
