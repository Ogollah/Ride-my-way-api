#/api/auth/views.py

from . import auth_blueprint

import re
from flask.views import MethodView
from flask import make_response, request, jsonify
from flask_jwt_extended import jwt_required, get_raw_jwt, create_access_token
from api.models import User, Ride, Request

blacklist = set()

class SignupView(MethodView):
    """Sign up view class"""

    def post(self):
        """Method to sighn up a new user"""
        add_data = request.data
        user_email = add_data['user_email']
        password = add_data['password']
        valid_email = re.match(
            "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", user_email)
        valid_password = re.match("[A-Za-z0-9@#$%^&+=]{4,}", password)
        if not valid_email:
            response = {"message": "Invalid email address."}
            return make_response(jsonify(response)), 400
        if not valid_password:
            return {"message": "Password should not be less than four characters."}, 400
        #Check if user already exists
        user = User.get_user_by_email(user_email=request.data['user_email'])
        if not user:
            #If there is no user try to add a new user
            try:
                add_user = User()
                add_user.user_email = user_email
                add_user.set_password_hash(password)
                add_user.save_user()

                response = {
                    "message": "Your have successfully signup for a new account."}
                #return a response of account creasion
                return make_response(jsonify(response)), 201
            except Exception as e:
                # An error occured, therefore return a string message containing the error

                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 401
        else:
            # Return a message to the user telling them that they they already exist
            response = {
                "message": "The email address has been used try another one."}
            return make_response(jsonify(response)), 409
          
class LoginView(MethodView):
    """Logging in registred user"""

    def post(self):
        """Method for logging in a signed up user"""
        user_email = request.data['user_email']
        registred_user = User.get_user_by_email(
            user_email=request.data['user_email'])
        if registred_user and registred_user.check_password_hash(request.data['password']):
            # Generate access token. This will be used as the authorization header
            access_token = create_access_token(identity=user_email)
            response = {'message': "You have successfully logged in!.",
                        "access_token": access_token}
            return make_response(jsonify(response)), 200
        else:
            # User does not exist. we return an error message
            response = {
                "message": "Invalid email or password, Please try again!"}
            return make_response(jsonify(response)), 401

class LogoutView(MethodView):
    """Logout Resource class."""
    @jwt_required
    def post(self):
        """Log out a given user by blacklisting user's token
        """
        jti = get_raw_jwt()['jti']
        blacklist.add(jti)
        response = {"message": "You have successfully logged out"}
        return make_response(jsonify(response)), 200

class ResetPasswordView(MethodView):
    """Reset password Resource class"""
    @jwt_required
    def post(self):
        """
            Reset password of a user
        """
        current_user = User.get_user_by_email(user_email=request.data['user_email'])
        new_password = request.data['new_password']
        if current_user and current_user.check_password_hash(request.data['old_password']):
            current_user.reset_password(new_password)
            current_user.set_password_hash(new_password)
            response = {
                'message': 'You have successfully reset your password.'}
            return make_response(jsonify(response)), 200
        else:
            response = {'message': 'Wrong password or email'}
            return make_response(jsonify(response)), 401


class CreateRideView(MethodView):
    """
        Create a new ride offer.
    """
    @jwt_required
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
                # An error occured, therefore return a string message containing the error
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
    @jwt_required
    def get(self):
        ride_offer_list = Ride.get_rides(self)
        #create a list of ride offers
        if ride_offer_list:
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
    @jwt_required
    def get(self,ride_id):
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
    @jwt_required
    def delete(self,ride_id):
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
    @jwt_required
    def put(self,ride_id):
        add_data = request.data
        new_start = add_data['new_start']
        new_stop = add_data['new_stop']
        new_date = add_data['new_date']
        new_time = add_data['new_time']
        #Check if business exists
        ride = Ride.get_ride_by_id(ride_id)
        if ride:
            ride.update_ride(
                new_start, new_stop, new_date, new_time)
            response = {"message": "Your ride is successfully updated!"}
            return make_response(jsonify(response)), 201
        else:
            response = {"message": "Ride offer you are looking for is not availbale"}
            return make_response(jsonify(response)), 404

class PostRequestView(MethodView):
    """
        Make a request view class.
    """
    
    @jwt_required
    def post(self,ride_id):
        ride_offer = Ride.get_ride_by_id(ride_id)
        if ride_offer:
            request = {"Ride": ride_offer.ride_name,
                        "Driver": ride_offer.driver, "Reg no": ride_offer.reg_num, "From": ride_offer.start,
                        "Destination": ride_offer.stop, "Passengers": ride_offer.passengers, "Time": ride_offer.time,
                        "Date": ride_offer.date, "Cost": ride_offer.cost}
            add_request = Request()
            add_request.request = request
            add_request.save_request()
            response = {
                "message": "Your ride request has been received successfully!"}
            return make_response(jsonify(response)), 200
        else:
            response = {
                "message": "The ride you are looking for is not available!"}
            return make_response(jsonify(response)), 404
# Define the API resource
#user
signup_view = SignupView.as_view('signup_view')
login_view = LoginView.as_view('login_view')
logout_view = LogoutView.as_view('logout_view')
reset_password_view = ResetPasswordView.as_view('reset_password_view')


#User
# Define the rule for the signup url --->  /api/v1/auth/signup
auth_blueprint.add_url_rule(
    '/api/v1/auth/signup',
    view_func=signup_view,
    methods=['POST'])

# Define the rule for the login url --->  /api/v1/auth/login
auth_blueprint.add_url_rule(
    '/api/v1/auth/login',
    view_func=login_view,
    methods=['POST'])

# Define the rule for the logout url --->  /api/v1/auth/logout
auth_blueprint.add_url_rule(
    '/api/v1/auth/logout',
    view_func=logout_view,
    methods=['POST'])

# Define the rule for the reset_password url --->  /api/v1/auth/reset_password
auth_blueprint.add_url_rule(
    '/api/v1/auth/reset-password',
    view_func=reset_password_view,
    methods=['POST'])

# Define the API resource
#Ride offer
ride_offer_view = CreateRideView.as_view('ride_offer_view')
get_ride_offers_view = GetRideView.as_view('get_ride_offers_view')
get_ride_offer_view = GetSingleRideView.as_view('get_ride_offer_view')
post_request_view = PostRequestView.as_view('post_request_view')

auth_blueprint.add_url_rule(
    '/api/v1/ride/create', view_func=ride_offer_view, methods=['POST'])
auth_blueprint.add_url_rule(
    '/api/v1/ride/rides', view_func=get_ride_offers_view, methods=['GET'])
auth_blueprint.add_url_rule(
    '/api/v1/ride/<int:ride_id>', view_func=get_ride_offer_view, methods=['GET', 'DELETE', 'PUT'])
auth_blueprint.add_url_rule(
    '/api/v1/ride/<int:ride_id>/request', view_func=post_request_view, methods=['POST'])
            





