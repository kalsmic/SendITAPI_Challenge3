# parcel.py
from .database import Database
from flask import jsonify



class ParcelOrder:

    def __init__(self):
        # create a database connection
        self.connect = Database()


    def parcel_details(self):

        """Returns the details of a parcel delivery order"""

        self.connect.cur.execute("SELECT * FROM parcels")
        parcels = self.connect.cur.fetchall()
        return parcels
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
