import folium
from geopy.geocoders import Nominatim
import pgeocode

def geocode_postal_code(postal_code):
    geolocator = Nominatim(user_agent="my_geocoder")
    location = geolocator.geocode(postal_code)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

# Geocode the location for Gatineau
gatineau_location = geocode_postal_code('J9H 3B4')

# Check if the location was successfully geocoded
if gatineau_location[0] is not None:
    # Create a map centered around Gatineau
    map = folium.Map(location=gatineau_location, zoom_start=12)

    # Optionally, add pothole locations here. For example:
    # pothole_locations = [('J8T 1W3', 'Pothole 1'), ('J8Y 6W6', 'Pothole 2')]
    # for code, name in pothole_locations:
    #     location = geocode_postal_code(code)
    #     if location[0] is not None:
    #         folium.Marker(location, popup=name).add_to(map)

    # Display the map
    display(map)
else:
    print("Failed to geocode the initial location.")
