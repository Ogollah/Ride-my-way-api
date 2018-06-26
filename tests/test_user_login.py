"""
This file holds user login test cases.
"""
import unittest
import json
from api import create_app


class AuthTestCase(unittest.TestCase):
    """
        Test case for User login.
    """

    def setUp(self):
        """Set up test variables."""
        self.app = create_app(config_name="testing")
        # initialize the test client
        self.client = self.app.test_client
        # This is the user test json data with a predefined email and password
        self.user_data = {
            'user_email': 'jimmy@example.com',
            'password': 'test_123'
        }
        self.user_data_log = {
            'user_email': 'lenny@example.com',
            'password': 'test_123'
        }
        self.not_a_user = {
            'user_email': 'abela@test.com',
            'password': 'nopekabisa'
        }

    def test_user_login(self):
        """Test signed up user can login."""
        response = self.client().post('/api/v1/auth/signup', data=self.user_data_log)
        self.assertEqual(response.status_code, 201)
        login_response = self.client().post('/api/v1/auth/login', data=self.user_data_log)
        #assert that the status code is equal to 200
        self.assertEqual(login_response.status_code, 200)
        #return result in json format
        result = json.loads(login_response.data.decode())
        #test that the response contains success message
        self.assertEqual(result["message"],
                         "You have successfully logged in!.")
        self.assertTrue(result["access_token"])

    def test_non_registered_user_login(self):
        """Test non registered users cannot login."""
        response = self.client().post('/api/v1/auth/signup', data=self.user_data)
        self.assertEqual(response.status_code, 201)
        # define a dictionary to represent an unregistered user
       
        #try to login with un registered user
        response = self.client().post('/api/v1/auth/login', data=self.not_a_user)
        #an error status code 401(Unauthorized)
        self.assertEqual(response.status_code, 401)
        # return result in json format
        result = json.loads(response.data.decode())
        # assert that this response must contain an error message)
        self.assertEqual(
            result['message'], "Invalid email or password, Please try again!")

if __name__ == '__main__':
    unittest.main()
