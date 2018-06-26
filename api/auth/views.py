#/api/auth/views.py

from . import auth_blueprint

import re
from flask.views import MethodView
from flask import make_response, request, jsonify
from flask_jwt_extended import jwt_required, get_raw_jwt, create_access_token
from api.models import User

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


# Define the API resource
#user
signup_view = SignupView.as_view('signup_view')
login_view = LoginView.as_view('login_view')
logout_view = LogoutView.as_view('logout_view')


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
