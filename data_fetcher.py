'''
data_faetcher.py
Hange Zhang CS5001 Spring 2024 Final Project
This module contains a function to fetch and clean data from a URL and store the results in a list of dictionaries.
'''
import requests
HTTP_SUCCESS = 200
LAT_INDEX = 0
LON_INDEX = 1


def fetch_data(url):
    """
    Purposes:
    Fetch CSV data from a URL.

    Parameters:
    url: The URL to fetch the CSV data from.

    Returns:
    str: The raw CSV data as a string.

    Raises:
    requests.HTTPError: If the request to the URL does not return a successful (200) status.
    """
    response = requests.get(url)
    if response.status_code != HTTP_SUCCESS:  # Check if the request was successful
        response.raise_for_status()  # Raise an exception if the request was not successful
    return response.text


def clean_data(csv_text, coord_column_name):
    """
    Purposes:
    Clean CSV data and store the results in a list of dictionaries with 'Lat' and 'Lon' keys.

    Parameters:
    csv_data: The raw CSV data as a string.
    coord_column_name: The name of the column containing the coordinate data.

    Returns:
    list of dict: A list where each item is a dictionary with 'Lat' and 'Lon' keys containing latitude and longitude data.

    Raises:
    ValueError: If the specified coordinates column does not exist in the data.
    ValueError: If the coordinates are invalid.
    """
    lines = csv_text.splitlines()
    headers = lines[0].split(';')
    clean_headers = []
    for header in headers:
        clean_header = header.replace('\ufeff', '')  # Remove BOM character if present reference: https://stackoverflow.com/questions/17912307/u-ufeff-in-python-string
        clean_headers.append(clean_header)

    if coord_column_name not in headers:
        raise ValueError(f"The specified coordinate column '{coord_column_name}' does not exist in the CSV data.")
    coord_index = headers.index(coord_column_name)

    results = []  # Initialize the results list
    for line in lines[1:]:  # Skip the header row
        entries = line.split(';')  # Split the line into individual entries
        if coord_index is not None:  # Check if the coordinate column exists
            if ',' not in entries[coord_index]:
                raise ValueError("Invalid coordinates.")
            coord = entries[coord_index].split(',')  # Split the coordinate data into latitude and longitude and store in a list
        else:
            coord = (None, None)

        lat, lon = coord[0].strip(), coord[1].strip()  # Extract the latitude and longitude
        if lat is None or lon is None:
            raise ValueError("Invalid coordinates.")
        lat, lon = float(lat), float(lon)  # Convert the latitude and longitude into floats

        if lat is not None and lon is not None:
            row_dict = {'Lat': lat, 'Lon': lon}
            for i in range(len(clean_headers)):
                row_dict[clean_headers[i]] = entries[i].strip()
            results.append(row_dict)

    return results
