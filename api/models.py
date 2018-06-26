"""
    Api models.
"""
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from flask import current_app
from datetime import datetime, timedelta

USERS = []


class User(object):
    """User model."""
    class_counter = 1

    def __init__(self):
        self.user_email = None
        self.password = None
        self.user_id = User.class_counter
        User.class_counter += 1

    def set_password_hash(self, password):
        """Set password hash."""
        self.password = generate_password_hash(password)

    def check_password_hash(self, password):
        """Check password hash."""
        return check_password_hash(self.password, password)

    @staticmethod
    def get_user_by_user_id(user_id):
        """Filter user by user_id."""
        for user in USERS:
            if user.user_id == user_id:
                return user

    @staticmethod
    def get_user_by_email(user_email):
        """Filter user by email."""
        for user in USERS:
            if user.user_email == user_email:
                return user

    def save_user(self):
        """Save a user in USERS."""
        USERS.append(self)

    def reset_password(self, new_password):
        """
        Update/reset the user password.
        """
        self.password = new_password
