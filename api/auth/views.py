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

class GetRideView(MethodView):
    """
        Get created ride offer.
    """

    def get(self):
        ride_offer_list = Ride.get_rides(self)
        #create a list of ride offers
        ride_offer = [{x.ride_id: [{"Ride": x.ride_name,
                                    "Driver": x.driver, "Reg no": x.reg_num, "From": x.start,
                                    "Destination": x.stop, "Passengers": x.passengers, "Time": x.time,
                                    "Date": x.date, "Cost": x.cost}] for x in ride_offer_list}]
        response = {"Available Rides": ride_offer}
        return make_response(jsonify(response)), 200

class GetSingleRideView(MethodView):
    """
        Get a single ride offer using ride_id class view.
    """

    def get(self, ride_id):
        """
            Get a ride offer by id method.
        """
        #Check if ride_offer exists
        ride_offer = Ride.get_ride_by_id(ride_id)
        if ride_offer:
            response = {"Ride": ride_offer.ride_name,
                        "Driver": ride_offer.driver, "Reg no": ride_offer.reg_num, "From": ride_offer.start,
                        "Destination": ride_offer.stop, "Passengers": ride_offer.passengers, "Time": ride_offer.time,
                        "Date": ride_offer.date, "Cost": ride_offer.cost}
            return make_response(jsonify(response)), 200
        else:
            response = {"message": "Your ride offer was not found!"}
            return make_response(jsonify(response)), 404

    def delete(self, ride_id):
            """
                Delete a ride by using its id
            """
            #Check if ride exists
            ride = Ride.get_ride_by_id(ride_id)
            if ride:
                ride.delete_ride(ride)
                response = {"message": "Ride offer successfully deleted!"}
                return make_response(jsonify(response)), 200
            else:
                response = {"message": "Not available"}
                return make_response(jsonify(response)), 404

# Define the API resource
#Ride offer
ride_offer_view = CreateRideView.as_view('ride_offer_view')
get_ride_offers_view = GetRideView.as_view('get_ride_offers_view')
get_ride_offer_view = GetSingleRideView.as_view('get_ride_offer_view')

auth_blueprint.add_url_rule(
    '/api/v1/ride/create', view_func=ride_offer_view, methods=['POST'])
auth_blueprint.add_url_rule(
    '/api/v1/ride/rides', view_func=get_ride_offers_view, methods=['GET'])
auth_blueprint.add_url_rule(
    '/api/v1/ride/<ride_id>', view_func=get_ride_offer_view, methods=['GET', 'DELETE'])
