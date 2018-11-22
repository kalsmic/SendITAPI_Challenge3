# parcel.py
from flask import jsonify

from .database import Database


class ParcelOrder:

    def __init__(self):
        # create a database connection
        self.connect = Database()

    def parcel_details(self):
        """Returns the details of a parcel delivery order"""

        self.connect.cursor.execute("SELECT * FROM parcels")

        parcels = self.connect.cursor.fetchall()
        return parcels

    def insert__a_parcel(self, item, pick_up_location, pick_up_date, destination, owner_id):
        # insert new parcel

        self.connect.cursor.execute("""INSERT INTO parcels(
        item, pick_up_location, pick_up_date, destination, owner_id) 
        VALUES ('{}','{}','{}','{}','{}')
        """.format(item, pick_up_location, pick_up_date, destination, owner_id))

    def cancel_a_parcel(self, parcel_id, owner_id, new_status):
        """Cancels a parcel delivery order"""

        self.connect.cursor.execute("SELECT status,owner_id from parcels where parcel_id='{}'".format(parcel_id))

        parcel = self.connect.cursor.fetchone()
        # parcel id does not exist
        if not parcel:
            return jsonify({'message':'Parcel does not exist'}),400

        if parcel['owner_id'] != owner_id:
            return jsonify({'message':"You're not allowed to perform this action"}),405

        if parcel['status'] != 'pending':
            return jsonify({'message':'Cannot cancel a parcel with status '+ parcel['status']})

        self.connect.cursor.execute("UPDATE parcels SET status ='{}' WHERE parcel_id='{}'"
                                    .format(new_status, parcel_id))
        return jsonify({'message':'Parcel status updated'}),200


# parcels = [ ]
# for parcel in parcels
# return {
#     'parcelId': parcels['parcel_id'],
#     "Item": parcels['.item'],
#     "destination": parcels['destination'],
#     "ownerId": parcels['owner_id'],
#     "pickUpLocation": parcels['pick_up_location'],
#     "pickUpDate": parcels['pick_up_date'],
#     "deliveredOn": parcels['delivered_on'],
#     "status": parcels['status']
# }

# def cancel_parcel_Order(self):
#     """Cancels a parcel delivery order"""
#     if self.status.upper() == 'PENDING':
#         # cancel Order
#         self.status = 'CANCELLED'
#
#         return True
#
#     # Order is already delivered,Cancelled,or In transit
#     return False

#
# parcelOrders = [
#     ParcelOrder('item', 'pickUp Address', 'Destination Address', 'pending', 1),
#     ParcelOrder('Laptop', 'Kampala', 'Moroto', 'Pending', 1),
#     ParcelOrder('Office Cabin', 'Kole', 'Otuke', 'In Transit', 2),
#     ParcelOrder('HMIS FORMS', 'Kitgum', 'Agago', 'Delivered', 1),
#     ParcelOrder('HRH PLANS', 'Yumbe', 'Koboko', 'Cancelled', 1),
#     ParcelOrder('DJ Mavic Air Beats', 'Mwanza', 'Bukoba', 'Cancelled', 1),
#     ParcelOrder('APPRAISAL FORMS', 'Mwanza', 'Bukoba', 'Pending', 2)
#
# ]
