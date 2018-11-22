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


    def update_parcel_status(self,parcelId, new_parcel_status):
        """Updates the status of the parcel delivery order"""

        self.connect.cursor.execute("SELECT status from parcels where parcel_id = '{}'".format(parcelId))
        parcel_status = self.connect.cursor.fetchone()
        parcel_status = parcel_status['status']

        if parcel_status.lower() in ['cancelled','delivered']:
            return jsonify({"message": "Cannot update parcel status for parcel with status "+ parcel_status}), 200


        if parcel_status.lower()== str(new_parcel_status).lower():
            return jsonify({"message":"Status already set to " + parcel_status}),200

        self.connect.cursor.execute("UPDATE parcels set status='{}' WHERE parcel_id='{}'".format(new_parcel_status, parcelId)),200
        return jsonify({"message":"Parcel status successfully updated to " + new_parcel_status}),200


