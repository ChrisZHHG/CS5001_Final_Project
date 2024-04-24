'''
visualization.py
Hange Zhang CS5001 Spring 2024 Final Project
This module contains a function to plot bikeways and washrooms on a map.
'''
import folium
from models.washroom import DEFAULT_RADIUS


def plot_locations(bikeways, washrooms, highlight_washroom=None):
    """
    Purposes:
    Plot bikeways and washrooms on a map using Folium.

    Parameters:
    bikeways: The Bikeway object containing bikeway data.
    washrooms: The Washroom object containing washroom data.
    highlight_washroom: Specific washroom to highlight on the map.

    Returns:
    None

    Raises:
    KeyError: If a key is missing in the bikeway details.
    """
    map_center = [49.2827, -123.1207]  # Vancouver's geographical center coordinates Reference see project—_design.pdf
    map = folium.Map(location=map_center, zoom_start=12)

    central_points = bikeways.get_central_points()
    washroom_density = washrooms.get_washroom_density(central_points, DEFAULT_RADIUS)

    # Plot each bikeway point
    for route, details in central_points.items():
        bikeway_info = (
            f"<strong>Route: {route}</strong><br>"
            f"Bikeway Type: {details.get('bikeway_type', 'N/A')}<br>"
            f"Speed Limit: {details.get('speed_limit', 'N/A')} mph<br>"  # Assuming speed limits are in mph
            f"Surface Type: {details.get('surface_type', 'N/A')}<br>"
            f"Year of Construction: {details.get('year_of_construction', 'N/A')}<br>"
            f"Nearby Washrooms: {washroom_density.get(route, 0)}"
        )
        try:
            folium.Marker(
                [details['lat'], details['lon']],
                popup=bikeway_info,
                icon=folium.Icon(color="green", icon="bicycle", prefix='fa')
            ).add_to(map)
        except KeyError as e:
            print(f"Missing key {e} in bikeway details for route {route}")

    # Plot each washroom point
    for washroom in washrooms.data:
        washroom_info = (
            f"<strong>{washroom['NAME']}</strong><br>"
            f"Wheel Access: {washroom.get('WHEEL_ACCESS', 'Unknown')}<br>"
            f"Hours: {washroom.get('SUMMER_HOURS', 'N/A')} (Summer), {washroom.get('WINTER_HOURS', 'N/A')} (Winter)"
        )
        color = "black" if highlight_washroom and washroom['NAME'] == highlight_washroom['NAME'] else "blue"
        folium.Marker(
            [washroom['Lat'], washroom['Lon']],
            popup=washroom_info,
            icon=folium.Icon(color=color, icon="restroom", prefix='fa')
        ).add_to(map)

    map.save('map.html')
