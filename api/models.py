"""
    Api models.
"""

#holds a list of ride offers
RIDES = []

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
