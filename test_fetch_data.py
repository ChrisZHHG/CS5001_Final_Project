'''
tests/test_data_fetcher.py
Hange Zhang CS5001 Spring 2024 Final Project
This module contains unit tests for the fetch_data and clean_data functions.
'''
import sys    # import sys module to access the path
sys.path.insert(0, '/Users/chriszhang/Desktop/Final')  # insert the path to the project folder

import unittest
import requests
import requests_mock
from models.data_fetcher import fetch_data, clean_data


class TestFetchData(unittest.TestCase):
    def test_fetch_data_success(self):
        with requests_mock.Mocker() as m:
            m.get('http://example.com/test.csv', text='id;name;lat;lon\n1;Place;34.0522,-118.2437')
            response = fetch_data('http://example.com/test.csv')
            self.assertIn('id;name;lat;lon', response)
            self.assertIn('Place', response)

    def test_fetch_data_failure(self):
        with requests_mock.Mocker() as m:
            m.get('http://example.com/test.csv', status_code=404)
            with self.assertRaises(requests.HTTPError):
                fetch_data('http://example.com/test.csv')


class TestCleanData(unittest.TestCase):
    def test_clean_data_success(self):
        csv_text = """\ufeffid;name;coordinates
                      1;Place One;34.0522,-118.2437
                      2;Place Two;35.0522,-119.2437"""
        expected_output = [
            {'id': '1', 'name': 'Place One', 'coordinates': '34.0522,-118.2437', 'Lat': 34.0522, 'Lon': -118.2437},
            {'id': '2', 'name': 'Place Two', 'coordinates': '35.0522,-119.2437', 'Lat': 35.0522, 'Lon': -119.2437}
        ]
        result = clean_data(csv_text.strip(), 'coordinates')
        self.assertEqual(result, expected_output)

    def test_clean_data_invalid_column(self):
        csv_text = "id;name;location\n1;Place One;34.0522,-118.2437"
        with self.assertRaises(ValueError) as context:
            clean_data(csv_text, 'coordinates')
        self.assertTrue("The specified coordinate column 'coordinates' does not exist in the CSV data." in str(context.exception))

    def test_clean_data_bad_coordinates(self):
        csv_text = "id;name;coordinates\n1;Place One;34.0522"
        with self.assertRaises(ValueError) as context:
            clean_data(csv_text, 'coordinates')
        self.assertTrue("Invalid coordinates." in str(context.exception))


if __name__ == '__main__':
    unittest.main()
