"""
This file holds user registration test cases.
"""
import unittest
import json
from api import create_app

class AuthTestCase(unittest.TestCase):
    """
        Test case for User registration.
    """

    def setUp(self):
        """Set up test variables."""
        self.app = create_app(config_name="testing")
        # initialize the test client
        self.client = self.app.test_client
        # This is the user test json data with a predefined email and password
        self.user_data = {
            'user_email': 'test@example.com',
            'password': 'test_123'
        }
        self.user_data_2 = {
            "user_email":"example@example.com",
            "password": "testexample"
        }
        self.user_data_3 = {
             "user_email": "example.com",
             "password": "testexample"
         }

        self.user_data_4 = {
            "user_email": "kelly@example.com",
            "password": "tes"
        }


    def test_user_signup(self):
        """Test user can signup for a new account."""
        response = self.client().post('/api/v1/auth/signup', data=self.user_data)
        self.assertEqual(response.status_code, 201)
        # return result in json format
        result = json.loads(response.data.decode())
        # assert that the request has a success message and a 201 status code
        self.assertEqual(result["message"],
                         "Your have successfully signup for a new account.")

    def test_already_signedup_user(self):
        """Test for dublicate signup."""
        response = self.client().post('/api/v1/auth/signup', data=self.user_data_2)
        self.assertEqual(response.status_code, 201)
        second_response = self.client().post('/api/v1/auth/signup', data=self.user_data_2)
        self.assertEqual(second_response.status_code, 202)
        # return result in json format
        result = json.loads(second_response.data.decode())
        self.assertEqual(
            result["message"], "The email address has been used try another one.")

    def test_valid_email(self):
        """Test for validity of email address used."""
        response = self.client().post('/api/v1/auth/signup', data=self.user_data_3)
        self.assertEqual(response.status_code, 202)
        # return result in json format
        result = json.loads(response.data.decode())
        self.assertEqual(
            result["message"], "Invalid email address.")

    def test_password_length(self):
        """Test user password should not be less than 4."""
        response = self.client().post('/api/v1/auth/signup', data=self.user_data_4)
        self.assertEqual(response.status_code, 202)
        # return result in json format
        result = json.loads(response.data.decode())
        self.assertEqual(
            result["message"], "Password should not be less than four characters.")

if __name__ == '__main__':
    unittest.main()
