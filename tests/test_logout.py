#tests/test_logout.py
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
            'user_email': 'test@example.com',
            'password': 'test_123'
        }

    def test_user_logout(self):
        """Test logged in user can logout."""
        response = self.client().post('/api/v1/auth/signup', data=self.user_data)
        self.assertEqual(response.status_code, 201)
        login_response = self.client().post('/api/v1/auth/login', data=self.user_data)
        self.assertEqual(login_response.status_code, 200)
        #Define header dictionary
        access_token = json.loads(login_response.data.decode())['access_token']
        logout_response = self.client().post('/api/v1/auth/logout',
                                             headers=dict(Authorization='Bearer ' + access_token), data=self.user_data)
        #assert that the status code is equal to 200
        self.assertEqual(logout_response.status_code, 200)
        #return result in json format
        result = json.loads(logout_response.data.decode())
        #test that the response contains success message
        self.assertEqual(result["message"], "You have successfully logged out")


if __name__ == '__main__':
    unittest.main()
