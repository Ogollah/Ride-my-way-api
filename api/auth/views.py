#/api/auth/views.py

from . import auth_blueprint

import re
from flask.views import MethodView
from flask import make_response, request, jsonify
from flask_jwt_extended import jwt_required, get_raw_jwt, create_access_token
from api.models import Ride

blacklist = set()


class CreateRideView(MethodView):
    """
        Create a new ride offer.
    """

    def post(self):
        """Method to create a new ride"""
        #Check if ride offer already exists
        ride_offer = Ride.get_ride_by_ride_name(ride_name=request.data['ride_name'])
        if not ride_offer:
            #If there is no ride_offer try to add a new ride_offer
            try:
                add_data = request.data
                ride_name = add_data['ride_name']
                driver = add_data['driver']
                reg_num = add_data['reg_num']
                start = add_data['start']
                stop = add_data['stop']
                passengers = add_data['passengers']
                time = add_data['time']
                date = add_data['date']
                cost = add_data['cost']
                add_ride_offer = Ride()
                add_ride_offer.ride_name = ride_name
                add_ride_offer.driver = driver
                add_ride_offer.reg_num = reg_num
                add_ride_offer.start = start
                add_ride_offer.stop = stop
                add_ride_offer.passengers = passengers
                add_ride_offer.time = time
                add_ride_offer.date = date
                add_ride_offer.cost = cost
                add_ride_offer.save_ride()

                response = {
                    "message": "Your ride offer has been added succesfully."}
                #return a response message and a status code
                return make_response(jsonify(response)), 201
            except Exception as e:
                # if an error occured, therefore return a string message containing the error
                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 401
        else:
            # Return a message to the user telling them that the ride offer already exist
            response = {
                "message": "You already have an active ride offer"}
            return make_response(jsonify(response)), 409

# Define the API resource
#Ride offer
ride_offer_view = CreateRideView.as_view('ride_offer_view')

auth_blueprint.add_url_rule(
    '/api/v1/ride/create', view_func=ride_offer_view, methods=['POST'])
