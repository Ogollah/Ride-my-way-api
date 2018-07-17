#tests/test_request.py
"""
This file holds ride offer request tests.
"""
import unittest
import json
from api import create_app


class RequestTestCase(unittest.TestCase):
    """Class for Ride offer request test cases"""

    def setUp(self):
        """Set up test variables."""
        self.app = create_app(config_name="testing")
        # initialize test client
        self.client = self.app.test_client
        
        self.user_data_sign = {
            'user_email': 'ngolo@example.com',
            'password': 'test_123'
        }
        self.user_data_2 = {
            'user_email': 'jumbo@example.com',
            'password': 'test_123'
        }
        self.ride_data_re = {
            "ride_name": "Mugumo's",
            "driver": "Martin Kamau",
            "reg_num": "KCS 124U",
            "start": "Kisauni",
            "stop": "Bamburi",
            "passengers": "4",
            "time": "10:00AM",
            "date": "21/6/2018",
            "cost": "KSH 5/KM "
        }
        self.ride_data_2 = {
             "ride_name": "Kanjo's",
             "driver": "Martin Kamau",
             "reg_num": "KCS 124U",
             "start": "Kisauni",
             "stop": "Bamburi",
             "passengers": "4",
             "time": "10:00AM",
             "date": "21/6/2018",
             "cost": "KSH 5/KM "
         }

    def test_request_ride(self):
        """
            Test that user can request a single ride offer using its id.
        """
        self.client().post('/api/v1/auth/signup', data=self.user_data_sign)
        login_response = self.client().post('/api/v1/auth/login', data=self.user_data_sign)
        #Define header dictionary
        access_token = json.loads(login_response.data.decode())['access_token']
        #create a new ride
        response = self.client().post('/api/v1/ride/create',
                                      headers=dict(Authorization='Bearer ' + access_token), data=self.ride_data_2)
        #get a ride using its id
        response = self.client().post('/api/v1/ride/1/request',
                                       headers=dict(Authorization='Bearer ' + access_token))
        #return message in json format
        result = json.loads(response.data.decode())
        #get a status code 200 and a success message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['message'],
                         "Your ride request has been received successfully!")

    def test_request_ride_with_invalid_id(self):
        """
            Test user cannot request for a ride offer which is not available.
        """
        self.client().post('/api/v1/auth/signup', data=self.user_data_2)
        login_response = self.client().post('/api/v1/auth/login', data=self.user_data_2)
        #Define header dictionary
        access_token = json.loads(login_response.data.decode())['access_token']
        #create a new ride
        response = self.client().post('/api/v1/ride/create', headers=dict(Authorization='Bearer ' + access_token), data=self.ride_data_re)
        response = self.client().post(
            '/api/v1/ride/7/request', headers=dict(Authorization='Bearer ' + access_token))
        #return message in json format
        result = json.loads(response.data.decode())
        #get a status code 404 and a success message
        self.assertEqual(response.status_code, 404)
        self.assertEqual(result['message'],
                         "The ride you are looking for is not available!")

    def test_get_ride_requests(self):
        """Test user can get a list of all ride requested."""
        self.client().post('/api/v1/auth/signup', data=self.user_data_2)
        login_response = self.client().post('/api/v1/auth/login', data=self.user_data_2)
        #Define header dictionary
        access_token = json.loads(login_response.data.decode())['access_token']
        #create a new ride
        response = self.client().post('/api/v1/ride/create',
                                      headers=dict(Authorization='Bearer ' + access_token), data=self.ride_data_re)
        self.client().post(
            '/api/v1/ride/7/request', headers=dict(Authorization='Bearer ' + access_token))
        response = self.client().get('/api/v1/1/ride/7/requests', headers=dict(Authorization='Bearer' + access_token))
        #get a status code 200
        self.assertEqual(response.status_code, 200)

    def test_get_ride_with_invalid_user_id_requests(self):
        """Test a wrong user cannot list of all ride requested using a wrong user id."""
        self.client().post('/api/v1/auth/signup', data=self.user_data_2)
        login_response = self.client().post('/api/v1/auth/login', data=self.user_data_2)
        #Define header dictionary
        access_token = json.loads(login_response.data.decode())['access_token']
        #create a new ride
        response = self.client().post('/api/v1/ride/create',
                                      headers=dict(Authorization='Bearer ' + access_token), data=self.ride_data_re)
        self.client().post(
            '/api/v1/ride/7/request', headers=dict(Authorization='Bearer ' + access_token))
        response = self.client().get('/api/v1/1/ride/7/requests',
                                     headers=dict(Authorization='Bearer' + access_token))
        result = json.loads(response.data.decode())
        #get a status code 200
        self.assertEqual(response.status_code, 401)
        self.assertEqual(result['message'], "You are not allowed to see view this list.")

    def test_get_a_ride_request(self):
        """Test user can get a sigle ride request."""
        self.client().post('/api/v1/auth/signup', data=self.user_data_2)
        login_response = self.client().post('/api/v1/auth/login', data=self.user_data_2)
        #Define header dictionary
        access_token = json.loads(login_response.data.decode())['access_token']
        #create a new ride
        self.client().post('/api/v1/ride/create',
                                      headers=dict(Authorization='Bearer ' + access_token), data=self.ride_data_re)
        self.client().post(
            '/api/v1/ride/7/request', headers=dict(Authorization='Bearer ' + access_token))
        response = self.client().get('/api/v1/1/ride/7/requests/1', headers=dict(Authorization='Bearer' + access_token))
        #get a status code 200
        self.assertEqual(response.status_code, 200)

    def test_get_ride_request_not_available(self):
        """Test user cannot get a ride request not made."""
        self.client().post('/api/v1/auth/signup', data=self.user_data_2)
        login_response = self.client().post('/api/v1/auth/login', data=self.user_data_2)
        #Define header dictionary
        access_token = json.loads(login_response.data.decode())['access_token']
        #create a new ride
        self.client().post('/api/v1/ride/create',
                                      headers=dict(Authorization='Bearer ' + access_token), data=self.ride_data_re)
        self.client().post('/api/v1/ride/7/request', headers=dict(Authorization='Bearer ' + access_token))
        response = self.client().get('/api/v1/1/ride/7/requests/5', headers=dict(Authorization='Bearer' + access_token))
        #return message in json format
        result = json.loads(response.data.decode())
        #get a status code 200 and a success
        self.assertEqual(response.status_code, 404)
        self.assertEqual(result['message'],
                         "Request you are looking for is not available")
        
    def test_accept_request(self):
        """Test user can accept a ride request."""
        self.client().post('/api/v1/auth/signup', data=self.user_data_2)
        login_response = self.client().post('/api/v1/auth/login', data=self.user_data_2)
        #Define header dictionary
        access_token = json.loads(login_response.data.decode())['access_token']
        #create a new ride
        self.client().post('/api/v1/ride/create',
                                      headers=dict(Authorization='Bearer ' + access_token), data=self.ride_data_re)
        self.client().post('/api/v1/ride/7/request', headers=dict(Authorization='Bearer ' + access_token))
        self.client().get('/api/v1/1/ride/7/requests/5', headers=dict(Authorization='Bearer' + access_token))
        response = self.client().post('/api/v1/1/ride/7/requests/5/respond',
                                      headers=dict(Authorization='Bearer' + access_token))
        #return message in json format
        result = json.loads(response.data.decode())
        #get a status code 200 and a success
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['message'],
                         "Your request has been accepted!")

    def test_reject_request(self):
        """Test user can accept a ride request."""
        self.client().post('/api/v1/auth/signup', data=self.user_data_2)
        login_response = self.client().post('/api/v1/auth/login', data=self.user_data_2)
        #Define header dictionary
        access_token = json.loads(login_response.data.decode())['access_token']
        #create a new ride
        self.client().post('/api/v1/ride/create',
                           headers=dict(Authorization='Bearer ' + access_token), data=self.ride_data_re)
        self.client().post('/api/v1/ride/7/request',
                           headers=dict(Authorization='Bearer ' + access_token))
        self.client().get('/api/v1/1/ride/7/requests/5',
                          headers=dict(Authorization='Bearer' + access_token))
        response = self.client().post('/api/v1/1/ride/7/requests/5/respond',
                                      headers=dict(Authorization='Bearer' + access_token))
        #return message in json format
        result = json.loads(response.data.decode())
        #get a status code 200 and a success
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['message'],
                         "Your request has been rejected!")

if __name__ == '__main__':
    unittest.main()
