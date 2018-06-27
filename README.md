[![Build Status](https://travis-ci.org/Ogollah/Ride-my-way-api.svg?branch=develop)](https://travis-ci.org/Ogollah/Ride-my-way-api)[![Coverage Status](https://coveralls.io/repos/github/Ogollah/Ride-my-way-api/badge.svg?branch=develop)](https://coveralls.io/github/Ogollah/Ride-my-way-api?branch=develop)
# Ride-my-way-api
Ride-my App is a carpooling application that provides drivers with the ability to create ride offers and passengers to join available ride offers.
   
# API Endpoints
|Endpoint                            | Functionality                    |HTTP method 
|------------------------------------|----------------------------------|-------------
|/api/v1/auth/signup                 |Create account                    |POST        
|/api/v1/auth/login                  |Login in user                     |POST
|/api/v1/auth/reset-passwor          |Change password                   |POST
|/api/v1/auth/logout                 |Signs out user                    |POST
|/api/v1/ride/create                 |Create a ride offer               |POST
|/api/v1/ride/rides                  |Fetch all ride offers             |GET
|/api/v1/ride/<ride_id>              |Fetch a single ride offer         |GET
|/api/v1/ride/<ride_id>              |Deletes a single ride offer       |DELETE
|/api/v1/ride/<ride_id>              |update a ride offer               |PUT 
|/api/v1/ride/<ride_id>/request      |Request a ride offer              |POST


### Quick Start

1. Clone the repo
  ```
  $ git clone https://github.com/Ogollah/Ride-my-way-api.git
  $ cd Ride-my-way-api
  ```

2. Initialize and activate a virtualenv:
  ```
  $ python3 -venv env
  $ source env/bin/activate
  ```

3. Install the dependencies:
  ```
  $ pip install -r requirements.txt
  ```

5. Run the development server:
  ```
  $ python run.py
  ```
  ```
  Or
  $ export FLASK_APP=run.py
  ```
  ```
  $ flask run
  ```

6. Navigate to [http://localhost:5000](http://localhost:5000)

# Project Owner
   Andela Kenya

# Developer
   [Stephen Ogolla](https://github.com/Ogollah/)
