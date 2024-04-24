'''
bikeway.py
Hange Zhang CS5001 Spring 2024 Final Project
This module contains the Bikeway class and calculate the central points for each bikeway route.
'''


class Bikeway:
    def __init__(self, data):
        """
        Purposes:
        Initialize bikeway instance with separate attributes for each field.

        Parameters:
        data: The data to initialize the bikeway instance with.

        Returns:
        Nothing

        Raises:
        Nothing
        """
        self.data = data
        self.route_names = []
        self.lats = []
        self.lons = []
        self.bikeway_types = []
        self.speed_limits = []
        self.surface_types = []
        self.years_of_construction = []

        for d in data:
            self.route_names.append(d['Bike Route Name'])
            self.lats.append(float(d['Lat']))
            self.lons.append(float(d['Lon']))
            self.bikeway_types.append(d['Bikeway Type'])
            self.speed_limits.append(d['Speed Limit'])
            self.surface_types.append(d['Surface Type'])
            self.years_of_construction.append(d['Year of Construction'])

    def get_central_points(self):
        """
        Purposes:
        Calculate the central points for each bikeway route.

        Parameters:
        Nothing

        Returns:
        central_points: Dictionary containing the central points for each bikeway route.

        Raises:
        Nothing
        """
        central_points = {}
        for i in range(len(self.route_names)):
            route_name = self.route_names[i]
            lat = self.lats[i]
            lon = self.lons[i]
            bikeway_type = self.bikeway_types[i]
            speed_limit = self.speed_limits[i]
            surface_type = self.surface_types[i]
            year_of_construction = self.years_of_construction[i]

            if route_name not in central_points:
                central_points[route_name] = {
                    'lats': [], 'lons': [], 'bikeway_type': bikeway_type or 'Unknown',
                    'speed_limits': [], 'surface_types': [], 'years_of_construction': []
                }

            central_points[route_name]['lats'].append(lat)
            central_points[route_name]['lons'].append(lon)
            central_points[route_name]['speed_limits'].append(speed_limit)
            central_points[route_name]['surface_types'].append(surface_type)
            central_points[route_name]['years_of_construction'].append(year_of_construction)

        for route_name, details in central_points.items():
            details['lat'] = sum(details['lats']) / len(details['lats'])
            details['lon'] = sum(details['lons']) / len(details['lons'])
            details['speed_limit'] = max(set(details['speed_limits']), key=details['speed_limits'].count)  # most common
            details['surface_type'] = max(set(details['surface_types']), key=details['surface_types'].count)  # most common
            details['year_of_construction'] = max(set(details['years_of_construction']), key=details['years_of_construction'].count)  # most common

        return central_points