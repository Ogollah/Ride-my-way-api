"""
This file holds ride offer tests.
"""
import unittest
import json
from api import create_app


class RideTestCase(unittest.TestCase):
    """Class for Ride test cases"""

    def setUp(self):
        """Set up test variables."""
        self.app = create_app(config_name="testing")
        # initialize test client
        self.client = self.app.test_client
        """ This is the create ride offer test json data with a predefined ride name, driver name, reg_num, start,
            stop, time, date and cost.
         """
        self.user_data = {
            'user_email': 'test@example.com',
            'password': 'test_123'
        }
        self.ride_data = {
            "ride_name": "Kamau's",
            "driver": "Martin Kamau",
            "reg_num": "KCS 124U",
            "start": "Kisauni",
            "stop": "Bamburi",
            "passengers": "4",
            "time": "10:00AM",
            "date": "21/6/2018",
            "cost": "KSH 5/KM "
        }
        self.ride_data_1 = {
            "ride_name": "Martin's",
            "driver": "Martin Kamau",
            "reg_num": "KCS 124U",
            "start": "Kisauni",
            "stop": "Bamburi",
            "passengers": "4",
            "time": "10:00AM",
            "date": "21/6/2018",
            "cost": "KSH 5/KM "
        }

        self.ride_data_update = {
            "start": "Kisauni",
            "new_stop": "Bamburi",
            "new_time": "10:00AM",
            "new_date": "21/6/2018"
        }

    def test_crete_a_ride_offer(self):
        """
            Test that a user can create a ride works correctly.
        """
        response = self.client().post('/api/v1/auth/signup', data=self.user_data)
        self.assertEqual(response.status_code, 201)
        login_response = self.client().post('/api/v1/auth/login', data=self.user_data)
        self.assertEqual(login_response.status_code, 200)
        #Define header dictionary
        access_token = json.loads(login_response.data.decode())['access_token']
        response = self.client().post('/api/v1/ride/create', headers=dict(Authorization='Bearer ' + access_token), data=self.ride_data)
        #return message in json format
        result = json.loads(response.data.decode())
        #assert that the request contains a success message and a 201 status code
        self.assertEqual(result['message'],
                         "Your ride offer has been added succesfully.")
        self.assertEqual(response.status_code, 201)

    def test_already_created_ride_offer(self):
        """
            Test a user cannot create more than one ride at a time.
        """
        response = self.client().post('/api/v1/auth/signup', data=self.user_data)
        self.assertEqual(response.status_code, 201)
        login_response = self.client().post('/api/v1/auth/login', data=self.user_data)
        self.assertEqual(login_response.status_code, 200)
        #Define header dictionary
        access_token = json.loads(login_response.data.decode())['access_token']
        #create a new ride offer
        response = self.client().post('/api/v1/ride/create', headers=dict(Authorization='Bearer ' + access_token), data=self.ride_data_1)
        #create the same ride offer again
        response = self.client().post('/api/v1/ride/create', headers=dict(Authorization='Bearer ' + access_token), data=self.ride_data_1)
        #return message in json format
        result = json.loads(response.data.decode())
        #assert that the reques a message and a 202 status code
        self.assertEqual(result['message'],
                         "You already have an active ride offer")
        self.assertEqual(response.status_code, 202)

    def test_view_ride_offer_list(self):
        """
            Test that a user can view a list of all rides on offer.
        """
        response = self.client().post('/api/v1/auth/signup', data=self.user_data)
        self.assertEqual(response.status_code, 201)
        login_response = self.client().post('/api/v1/auth/login', data=self.user_data)
        self.assertEqual(login_response.status_code, 200)
        #Define header dictionary
        access_token = json.loads(login_response.data.decode())['access_token']
        #create a new ride offer
        response = self.client().post('/api/v1/ride/create', headers=dict(Authorization='Bearer ' + access_token), data=self.ride_data)
        #get a list of all ride offers.
        response = self.client().get('/api/v1/ride/rides',
                                     headers=dict(Authorization='Bearer ' + access_token))
        #assert that the status code is 200
        self.assertEqual(response.status_code, 200)

    def test_view_a_ride_by_id(self):
        """
            Test that user can get a single ride offer using its id.
        """
        response = self.client().post('/api/v1/auth/signup', data=self.user_data)
        self.assertEqual(response.status_code, 201)
        login_response = self.client().post('/api/v1/auth/login', data=self.user_data)
        self.assertEqual(login_response.status_code, 200)
        #Define header dictionary
        access_token = json.loads(login_response.data.decode())['access_token']
        #create a new ride
        response = self.client().post('/api/v1/rides/create', headers=dict(Authorization='Bearer ' + access_token), data=self.ride_data)
        self.assertEqual(response.status_code, 201)
        #get a ride using its id
        response = self.client().get(
            '/api/v1/ride/1', headers=dict(Authorization='Bearer ' + access_token))
        # assert that the status code is 200
        self.assertEqual(response.status_code, 200)

    def test_can_not_view_unavailable_ride_by_id(self):
        """
            Test a user view ride offer that has either been deleted, expired, or not created.
        """
        response = self.client().post('/api/v1/auth/signup', data=self.user_data)
        self.assertEqual(response.status_code, 201)
        login_response = self.client().post('/api/v1/auth/login', data=self.user_data)
        self.assertEqual(login_response.status_code, 200)
        #Define header dictionary
        access_token = json.loads(login_response.data.decode())['access_token']
        #create a new ride
        response = self.client().post('/api/v1/rides/create', headers=dict(Authorization='Bearer ' + access_token), data=self.ride_data)
        self.assertEqual(response.status_code, 201)
        #get a ride using its id
        response = self.client().get(
            '/api/v1/ride/2', headers=dict(Authorization='Bearer ' + access_token))
        #return message in json format
        result = json.loads(response.data.decode())
        # assert that the status code is 404 and not available message
        self.assertEqual(result['message'],
                         "Your ride offer was not found!")
        self.assertEqual(response.status_code, 404)

    def test_delete_a_ride_by_id(self):
        """
            Test a user can delete a ride offer using its id.
        """
        response = self.client().post('/api/v1/auth/signup', data=self.user_data)
        self.assertEqual(response.status_code, 201)
        login_response = self.client().post('/api/v1/auth/login', data=self.user_data)
        self.assertEqual(login_response.status_code, 200)
        #Define header dictionary
        access_token = json.loads(login_response.data.decode())['access_token']
        #create a new ride
        response = self.client().post('/api/v1/rides/create', headers=dict(Authorization='Bearer ' + access_token), data=self.ride_data)
        #delete a ride by id
        response = self.client().delete(
            '/api/v1/ride/1', headers=dict(Authorization='Bearer ' + access_token))
        #return message in json format
        result = json.loads(response.data.decode())
        #assert that the request contains a success message and a 200 status code
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['message'], 'Ride offer successfully deleted!')
        #test to see if its still available
        response = self.client().get('/api/v1/ride/1')
        #assert that the status code is 404
        self.assertEqual(response.status_code, 404)

    def test_delete_with_invalide_id(self):
        """
            Test a user can not delete a ride offer which is not available.
        """
        response = self.client().post('/api/v1/auth/signup', data=self.user_data)
        self.assertEqual(response.status_code, 201)
        login_response = self.client().post('/api/v1/auth/login', data=self.user_data)
        self.assertEqual(login_response.status_code, 200)
        #Define header dictionary
        access_token = json.loads(login_response.data.decode())['access_token']
        #create a new ride
        response = self.client().post('/api/v1/rides/create', headers=dict(Authorization='Bearer ' + access_token), data=self.ride_data)
        self.assertEqual(response.status_code, 201)
        response = self.client().delete(
            '/api/v1/ride/2', headers=dict(Authorization='Bearer ' + access_token))
        #return message in json format
        result = json.loads(response.data.decode())
        #assert that the request contains a success message and a 200 status code
        self.assertEqual(response.status_code, 204)
        self.assertEqual(result['message'], 'Not available')

    def test_update_ride_offer(self):
        """
            Test a user can update details of a ride offer. 
        """
        response = self.client().post('/api/v1/auth/signup', data=self.user_data)
        self.assertEqual(response.status_code, 201)
        login_response = self.client().post('/api/v1/auth/login', data=self.user_data)
        self.assertEqual(login_response.status_code, 200)
        #Define header dictionary
        access_token = json.loads(login_response.data.decode())['access_token']
        #create a new ride
        response = self.client().post('/api/v1/ride/create', headers=dict(Authorization='Bearer ' + access_token), data=self.ride_data)
        self.assertEqual(response.status_code, 201)
        response = self.client().put('/api/v1/ride/1', headers=dict(Authorization='Bearer ' + access_token), data=self.ride_data_update)
        #return message in json format
        result = json.loads(response.data.decode())
        #get a status code 201 and a success message
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result['message'],
                         "Your ride is successfully updated!")

    def test_update_with_invalid_id(self):
        """
            Test a user can not update a ride which is not available.
        """
        response = self.client().post('/api/v1/auth/signup', data=self.user_data)
        self.assertEqual(response.status_code, 201)
        login_response = self.client().post('/api/v1/auth/login', data=self.user_data)
        self.assertEqual(login_response.status_code, 200)
        #Define header dictionary
        access_token = json.loads(login_response.data.decode())['access_token']
        #create a new ride
        response = self.client().post('/api/v1/ride/create', headers=dict(Authorization='Bearer ' + access_token), data=self.ride_data)
        self.assertEqual(response.status_code, 201)
        response = self.client().put('/api/v1/ride/3', headers=dict(Authorization='Bearer ' + access_token), data=self.ride_data_update)
        #return message in json format
        result = json.loads(response.data.decode())
        #get a status code 204 and a success message
        self.assertEqual(response.status_code, 204)
        self.assertEqual(result['message'],
                         "Ride offer you are looking for is not availbale")

if __name__ == '__main__':
    unittest.main()
