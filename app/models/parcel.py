# parcel.py
from flask import jsonify

from .database import Database
from app.helpers import get_current_user_id

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
        item, pick_up_location,present_location, pick_up_date, destination, owner_id) 
        VALUES ('{}','{}','{}','{}','{}','{}')
        """.format(item, pick_up_location, pick_up_location, pick_up_date, destination, owner_id))

    def cancel_a_parcel(self, parcel_id, owner_id, new_status):
        """Cancels a parcel delivery order"""

        self.connect.cursor.execute("SELECT status,owner_id from parcels where parcel_id='{}'".format(parcel_id))

        parcel = self.connect.cursor.fetchone()
        # parcel id does not exist
        if not parcel:
            return jsonify({'message': 'Parcel does not exist'}), 400

        if parcel['owner_id'] != owner_id:
            return jsonify({'message': "You're not allowed to perform this action"}), 405

        if parcel['status'] != 'pending':
            return jsonify({'message': 'Cannot cancel a parcel with status ' + parcel['status']})

        self.connect.cursor.execute("UPDATE parcels SET status ='{}' WHERE parcel_id='{}'"
                                    .format(new_status, parcel_id))
        return jsonify({'message': 'Parcel status updated'}), 200

    def update_parcel_status(self, parcelId, new_parcel_status):
        """Updates the status of the parcel delivery order"""

        self.connect.cursor.execute("SELECT status from parcels where parcel_id = '{}'".format(parcelId))
        parcel_status = self.connect.cursor.fetchone()

        if not parcel_status:
            return jsonify({'message': 'Parcel does not exist'}), 400

        parcel_status = parcel_status['status']

        if parcel_status.lower() in ['cancelled', 'delivered']:
            return jsonify({"message": "Cannot update parcel status for parcel with status " + parcel_status}), 200

        # Check if status is already set to the same
        if parcel_status.lower() == str(new_parcel_status).lower():
            return jsonify({"message": "Status already set to " + parcel_status}), 200

        self.connect.cursor.execute(
            "UPDATE parcels set status='{}' WHERE parcel_id='{}'".format(new_parcel_status, parcelId))
        return jsonify({"message": "Parcel status successfully updated to " + new_parcel_status}), 200

    def update_parcel_present_location(self, parcelId, new_present_location):
        """Updates the status of the parcel delivery order"""

        self.connect.cursor.execute("SELECT status from parcels where parcel_id = '{}'".format(parcelId))
        current_parcel_status = self.connect.cursor.fetchone()

        if not current_parcel_status:
            return jsonify({'message': 'Parcel does not exist'}), 400

        current_parcel_status = current_parcel_status['status']

        if current_parcel_status.lower() in ['cancelled', 'delivered']:
            # Check if parcel is already delivered or  cancelled
            return jsonify({"message": "Cannot update present location of a " + current_parcel_status
                                       + " parcel delivery order"}), 403

        self.connect.cursor.execute("UPDATE parcels set present_location='{}' WHERE parcel_id='{}'"
                                    .format(new_present_location, parcelId))

        return jsonify({"message": "Parcel's present location updated to " + new_present_location}), 200


    def update_parcel_destination_address(self, parcelId, new_destination_address):
        """Updates the status of the parcel delivery order"""

        self.connect.cursor.execute("SELECT status,owner_id from parcels where parcel_id = '{}'".format(parcelId))
        current_parcel_details = self.connect.cursor.fetchone()

        if not current_parcel_details:
            return jsonify({'message': 'Parcel does not exist'}), 400

        current_parcel_status = current_parcel_details['status']
        current_parcel_owner = current_parcel_details['owner_id']

        # check if parcel belongs to current user
        if current_parcel_owner != get_current_user_id():
            return jsonify({"message":"You are not allowed to modify this resource"}),403


        if current_parcel_status.lower() != 'pending':
            # Can only update destination of a parcel who's status is is pending
            return jsonify({"message": "Cannot update present location of  " + current_parcel_status
                                       + " parcel delivery order"}), 403

        self.connect.cursor.execute("UPDATE parcels set destination='{}' WHERE parcel_id='{}'"
                                    .format(new_destination_address, parcelId))

        return jsonify({"message": "Parcel's destination address updated to " + new_destination_address}), 200