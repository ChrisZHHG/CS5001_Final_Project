'''
data_dashboard.py
Hange Zhang CS5001 Spring 2024 Final Project
This module contains the main function to run the data dashboard program.
'''
from models.data_fetcher import fetch_data, clean_data
from models.bikeway import Bikeway
from models.washroom import Washroom
from views.visualization import plot_locations
from views import user_cli
from geopy.distance import geodesic

# URLs for data sources
BIKEWAYS_URL = 'https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/bikeways/exports/csv?lang=en&timezone=America%2FLos_Angeles&use_labels=true&delimiter=%3B'
WASHROOMS_URL = 'https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/public-washrooms/exports/csv?lang=en&timezone=America%2FLos_Angeles&use_labels=true&delimiter=%3B'


def find_nearest_washrooms(bikeway_name, bikeways, washrooms):
    """
    Purposes:
    Find the nearest washroom to a specific bikeway.

    Parameters:
    bikeway_name: The name of the bikeway to find the nearest washroom to.
    bikeways: The Bikeway object containing bikeway data.
    washrooms: The Washroom object containing washroom data.

    Returns:
    Nothing

    Raises:
    ValueError: If the bikeway name does not exist in the data.
    """
    central_points = bikeways.get_central_points()

    if bikeway_name not in central_points:
        raise ValueError("Bikeway name does not exist. Please enter a valid bikeway name")

    bikeway_point = central_points[bikeway_name]  # Get the central point of the bikeway
    bikeway_lat_lon = (bikeway_point['lat'], bikeway_point['lon'])  # Get the latitude and longitude of the bikeway

    min_distance = float('inf')  # Initialize the minimum distance to infinity
    nearest_washroom = None

    for washroom in washrooms.data:
        washroom_lat_lon = (washroom['Lat'], washroom['Lon'])
        distance = geodesic(bikeway_lat_lon, washroom_lat_lon).meters
        if distance < min_distance:
            min_distance = distance
            nearest_washroom = {
                'NAME': washroom['NAME'],
                'Lat': washroom['Lat'],
                'Lon': washroom['Lon'],
                'WHEEL_ACCESS': washroom['WHEEL_ACCESS'],
                'SUMMER_HOURS': washroom['SUMMER_HOURS'],
                'WINTER_HOURS': washroom['WINTER_HOURS']
            }
    if nearest_washroom:
        washroom_info = (
            f"Name: {nearest_washroom['NAME']}\n"
            f"Wheel Access: {nearest_washroom['WHEEL_ACCESS']}\n"
            f"Hours: {nearest_washroom['SUMMER_HOURS']} (Summer), {nearest_washroom['WINTER_HOURS']} (Winter)\n"
        )
        print(f"Nearest washroom to {bikeway_name} is approximately {min_distance:.2f} meters away:\n{washroom_info}")
        plot_locations(bikeways, washrooms, highlight_washroom=nearest_washroom)
        print("The map with the highlighted washroom has been generated and saved to map.html.")
    else:
        print("No nearby washroom could be found.")


def fetch_and_clean_data(url, coord_column_name='geo_point_2d'):
    """
    Fetch data from a URL and clean it.

    Parameters:
    url - URL from which to fetch data.
    coord_column_name - The name of the column in the CSV that contains coordinate data.

    Returns:
    list of dict - Cleaned data ready to be used to create data models.

    Raises:
    requests.HTTPError: If the data cannot be fetched.
    ValueError: If the data cannot be cleaned properly.
    """
    raw_csv = fetch_data(url)
    return clean_data(raw_csv, coord_column_name)


def create_objects(bikeways_data, washrooms_data):
    """
    Purposes:
    Create Bikeway and Washroom objects from cleaned data.

    Parameters:
    bikeways_data - Cleaned bikeways data.
    washrooms_data - Cleaned washrooms data.

    Returns:
    Bikeway, Washroom - The created data models.

    Raises:
    Nothing
    """
    bikeways = Bikeway(bikeways_data)
    washrooms = Washroom(washrooms_data)
    return bikeways, washrooms


def main():
    try:
        # Fetch and clean data, call the fetch_and_clean_data function
        bikeways_data = fetch_and_clean_data(BIKEWAYS_URL)
        washrooms_data = fetch_and_clean_data(WASHROOMS_URL)

        # Create Bikeway and Washroom objects
        bikeways, washrooms = create_objects(bikeways_data, washrooms_data)

        running = True
        while running:
            choice = user_cli.display_menu()
            if choice == '1':
                plot_locations(bikeways, washrooms)
                print("The map has been generated and saved to map.html.")
            elif choice == '2':
                bikeway_name = user_cli.get_bikeway_name()
                find_nearest_washrooms(bikeway_name, bikeways, washrooms)
            elif choice == '3':
                print("Exiting the program.")
                running = False
            else:
                print("Invalid input. Please enter a number between 1 and 3.")
    except ValueError as ve:
        print(f"Value Error: {ve}")
    except RuntimeError as re:
        print(f"Runtime Error: {re}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
