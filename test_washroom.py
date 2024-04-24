'''
tests/test_washroom.py
Hange Zhang CS5001 Spring 2024 Final Project
This module contains unit tests for the Washroom class.
'''
import sys  # import sys module to access the path
sys.path.insert(0, '/Users/chriszhang/Desktop/Final')  # insert the path to the project folder

import unittest
from models.washroom import Washroom


class TestWashroom(unittest.TestCase):
    def setUp(self):
        self.mock_data = [
            {'NAME': 'Washroom 1', 'Lat': '34.0522', 'Lon': '-118.2437', 'WHEEL_ACCESS': 'Yes', 'SUMMER_HOURS': '9-5', 'WINTER_HOURS': '10-4'},
            {'NAME': 'Washroom 2', 'Lat': '35.0522', 'Lon': '-119.2437', 'WHEEL_ACCESS': 'No', 'SUMMER_HOURS': '8-4', 'WINTER_HOURS': '9-3'}
        ]

    def test_initialization(self):
        washroom = Washroom(self.mock_data)
        self.assertEqual(len(washroom.names), 2)
        self.assertIn('Washroom 1', washroom.names)
        self.assertEqual(washroom.lats, [34.0522, 35.0522])

    def test_get_washroom_density(self):
        washroom = Washroom(self.mock_data)
        bikeway_central_points = {'Route 1': {'lat': 34.0522, 'lon': -118.2437}}
        density = washroom.get_washroom_density(bikeway_central_points)
        self.assertEqual(density['Route 1'], 1)


if __name__ == '__main__':
    unittest.main()
