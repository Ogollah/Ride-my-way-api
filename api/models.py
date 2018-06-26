"""
    Api models.
"""

#holds a list of ride offers
RIDES = []
REQUESTS = []

class Ride(object):
    """
        Ride class model.
    """
    class_counter = 1

    def __init__(self):
        """
            Initializes ride details.
        """
        self.ride_name = None
        self.driver = None
        self.reg_num = None
        self.start = None
        self.stop = None
        self.passengers = None
        self.time = None
        self.date = None
        self.cost = None
        self.ride_id = Ride.class_counter
        Ride.class_counter += 1

    def update_ride(self, new_start, new_stop, new_time, new_date):
        """This is a method for updating ride offer."""
        self.start = new_start
        self.stop = new_stop
        self.time = new_time
        self.date = new_date

    @staticmethod
    def get_ride_by_id(ride_id):
        """Get ride by it's id."""
        for ride in RIDES:
            if ride.ride_id == ride_id:
                return ride

    @staticmethod
    def get_ride_by_ride_name(ride_name):
        """Filter ride by ride_name."""
        for ride in RIDES:
            if ride.ride_name == ride_name:
                return ride

    @staticmethod
    def get_rides(self):
        """Get all rides."""
        return RIDES

    def save_ride(self):
        """Save a ride in RIDES list."""
        RIDES.append(self)
    
    @staticmethod
    def delete_ride(self):
        """Delete a ride method."""
        RIDES.remove(self)

class Request(object):
    """
        Ride class model.
    """
    class_counter = 1

    def __init__(self):
        """
            initializes request details.
        """
        self.request=None
        self.ride_id = Ride.class_counter
        Ride.class_counter += 1

    def save_request(self):
        """Save a request in the list of requests."""
        REQUESTS.append(self)


            
