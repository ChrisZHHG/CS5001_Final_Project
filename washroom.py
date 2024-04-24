'''
washroom.py
Hange Zhang CS5001 Spring 2024 Final Project
This module contains the Washroom class and calculate the density of nearby washrooms for each bikeway central point.
'''

from geopy.distance import geodesic
DEFAULT_RADIUS = 1000


class Washroom:
    def __init__(self, data):
        """
        Purpose:
        Initialize washroom instance with separate attributes for each field.

        Parameters:
        data: The data to initialize the washroom instance with.

        Returns:
        Nothing

        Raises:
        Nothing
        """
        self.data = data
        self.names = []
        self.lats = []
        self.lons = []
        self.wheel_accesses = []
        self.summer_hours = []
        self.winter_hours = []

        for d in data:
            self.names.append(d['NAME'])
            self.lats.append(float(d['Lat']))
            self.lons.append(float(d['Lon']))
            self.wheel_accesses.append(d['WHEEL_ACCESS'])
            self.summer_hours.append(d['SUMMER_HOURS'])
            self.winter_hours.append(d['WINTER_HOURS'])

    def get_washroom_density(self, bikeway_central_points, radius=DEFAULT_RADIUS):
        """
        Purpose:
        Calculate the density of washrooms within a specified radius for each bikeway central point.

        Parameters:
        bikeway_central_points: Dictionary containing bikeway central points.
        radius: The default radius to search for washrooms around each bikeway central point.

        Returns:
        washroom_density: Dictionary containing the number of washrooms within the default radius.

        Raises:
        Nothing
        """
        washroom_density = {}
        for route, point in bikeway_central_points.items():
            count = 0
            bikeway_lat = point['lat']
            bikeway_lon = point['lon']
            for i in range(len(self.lats)):
                washroom_lat = self.lats[i]
                washroom_lon = self.lons[i]
                if geodesic((bikeway_lat, bikeway_lon), (washroom_lat, washroom_lon)).meters <= radius:
                    count += 1
            washroom_density[route] = count
        return washroom_density
