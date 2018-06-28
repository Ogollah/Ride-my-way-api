#tests/test_password.py
import unittest
import json
from api import create_app


class UserLogoutTestCase(unittest.TestCase):
    """User logout taste cases class ."""

    def setUp(self):
        """Set up test variables."""
        self.app = create_app(config_name="testing")
        # initialize the test client
        self.client = self.app.test_client
        # This is the user test json data with a predefined username, email and password
        
        self.user_data = {
            'user_email': 'looky@example.com',
            'password': 'testexample'
        }
        self.user_data_2 = {
            'user_email': 'example@example.com',
            'password': 'test_123'
        }

    def test_user_can_reset_password(self):
        """Test user can change there password given correct credentials."""
        response = self.client().post('/api/v1/auth/signup', data=self.user_data)
        self.assertEqual(response.status_code, 201)
        login_response = self.client().post('/api/v1/auth/login', data=self.user_data)
        self.assertEqual(login_response.status_code, 200)
        #Define header dictionary
        access_token = json.loads(login_response.data.decode())['access_token']
        reset_password = {
            "user_email": "looky@example.com",
            "old_password": "testexample",
            "new_password": "123456"
        }
        reset_response = self.client().post('/api/v1/auth/reset-password',
                                       headers=dict(Authorization='Bearer ' + access_token), data=reset_password)
        #assert that the status code is equal to 200
        self.assertEqual(reset_response.status_code, 200)
        #return result in json format
        result = json.loads(reset_response.data.decode())
        #test that the response contains success message
        self.assertEqual(result["message"],
                         "You have successfully reset your password.")
        

    def test_user_cannot_reset_password_with_invalid_credential(self):
        """Test user cannot change there password given incorrect credentials."""
        response = self.client().post('/api/v1/auth/signup', data=self.user_data_2)
        self.assertEqual(response.status_code, 201)
        login_response = self.client().post('/api/v1/auth/login', data=self.user_data_2)
        self.assertEqual(login_response.status_code, 200)
        #Define header dictionary
        access_token = json.loads(login_response.data.decode())['access_token']
        reset_password = {
            "user_email": "example@example.com",
            "old_password": "exampletest",
            "new_password": "123456"
        }
        reset_response = self.client().post('/api/v1/auth/reset-password',
                                       headers=dict(Authorization='Bearer ' + access_token), data=reset_password)
        #assert that the status code is equal to 401
        self.assertEqual(reset_response.status_code, 401)
        #return result in json format
        result = json.loads(reset_response.data.decode())
        #test that the response contains a message
        self.assertEqual(result["message"],
                         "Wrong password or email")


if __name__ == '__main__':
    unittest.main()
