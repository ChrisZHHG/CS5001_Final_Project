'''
tests/test_bikeway.py
Hange Zhang CS5001 Spring 2024 Final Project
This module contains unit tests for the Bikeway class.
'''
import sys  # import sys module to access the path
sys.path.insert(0, '/Users/chriszhang/Desktop/Final')  # insert the path to the project folder

import unittest
from models.bikeway import Bikeway


class TestBikeway(unittest.TestCase):
    def setUp(self):
        self.mock_data = [
            {'Bike Route Name': 'Route 1', 'Lat': '34.0522', 'Lon': '-118.2437', 'Bikeway Type': 'Type A', 'Speed Limit': '25', 'Surface Type': 'Asphalt', 'Year of Construction': '2010'},
            {'Bike Route Name': 'Route 2', 'Lat': '34.0522', 'Lon': '-118.2437', 'Bikeway Type': 'Type B', 'Speed Limit': '30', 'Surface Type': 'Concrete', 'Year of Construction': '2015'}
        ]

    def test_initialization(self):
        bikeway = Bikeway(self.mock_data)
        self.assertEqual(len(bikeway.route_names), 2)
        self.assertEqual(bikeway.route_names, ['Route 1', 'Route 2'])
        self.assertEqual(bikeway.lats, [34.0522, 34.0522])
        self.assertEqual(bikeway.lons, [-118.2437, -118.2437])

    def test_get_central_points(self):
        bikeway = Bikeway(self.mock_data)
        central_points = bikeway.get_central_points()
        self.assertIsInstance(central_points, dict)
        self.assertIn('Route 1', central_points)
        self.assertAlmostEqual(central_points['Route 1']['lat'], 34.0522)
        self.assertAlmostEqual(central_points['Route 1']['lon'], -118.2437)


if __name__ == '__main__':
    unittest.main()
