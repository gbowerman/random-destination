"""randomdest.py - dearpygui app to plot random destinations"""
import math
import os
import random

import requests
from dotenv import load_dotenv

from dearpygui.core import *
from dearpygui.simple import *

# globals/constants
EARTH_RADIUS = 6378.1
MAX_DIST = 16 # destination radius in KM
maps_key = ""
BASE_URL = "https://dev.virtualearth.net/REST/v1/Imagery/Map/AerialWithLabels/"
zoom = "15"
img_size_x = 900
img_size_y = 900
img_file_name = "pic1.png"


def plot_location(latitude, longitude, bearing, distance):
    '''Plot a new location based on starting point, bearing and distance'''
    bearing_rad = math.radians(bearing) 

    lat1 = math.radians(latitude)
    lon1 = math.radians(longitude)

    d_over_r = distance/EARTH_RADIUS

    lat2 = math.asin(math.sin(lat1)*math.cos(d_over_r) +
        math.cos(lat1)*math.sin(d_over_r)*math.cos(bearing_rad))

    lon2 = lon1 + math.atan2(math.sin(bearing_rad)*math.sin(d_over_r)*math.cos(lat1),
                math.cos(d_over_r)-math.sin(lat1)*math.sin(lat2))

    lat2 = round(math.degrees(lat2), 6)
    lon2 = round(math.degrees(lon2), 6)

    return [lat2,lon2]


def get_random_location(latitude, longitude, radius_km):
    '''Return coordinates for a random location based on starting point and radius'''

    # get random destination and distance
    bearing = random.randint(0,360)
    distance_km = round(radius_km * random.random(),3)
    #print(f"Bearing: {str(bearing)}, Distance (km): {str(distance_km)}")
    set_value("bearing_label", f"Bearing: {str(bearing)}°, Distance: {str(distance_km)} km")
    
    # calculate the new latitude and longitude
    return plot_location(latitude, longitude, bearing, distance_km)


def get_image(coords):
    '''Get a new Bing maps image for specified coordinates and save it as a PNG file'''
    pic_url = f"{BASE_URL}{coords}/{zoom}?mapSize={str(img_size_x)},{str(img_size_y)}&pp={coords};;1&dcl=1&key={maps_key}"
    image_data = requests.get(pic_url).content
    with open(img_file_name, "wb") as handler:
        handler.write(image_data)


def get_route_image(coords1, coords2):
    '''Get a new Bing maps image for specified coordinates and save it as a PNG file'''
    pic_url = f"{BASE_URL}{coords1}/12/Routes/Driving?waypoint.1={coords1}&waypoint.2={coords2}&mapSize={str(img_size_x)},{str(img_size_y)}&imagerySet=AerialWithLabels&key={maps_key}"
    image_data = requests.get(pic_url).content
    with open(img_file_name, "wb") as handler:
        handler.write(image_data)


def show_origin(sender, callback):
    '''Get the coordinates from the UI and get the Bing maps image for those coords'''
    coords = get_value("Coords")
    get_image(coords)

    # update canvas
    clear_drawing("canvas")
    draw_image("canvas", img_file_name, [0, 0], pmax=[img_size_x, img_size_y])


def show_destination(sender, callback):
    '''Display a map image for the destination coordinates'''
    coords = get_value("destination_text")
    get_image(coords)

    # update canvas
    clear_drawing("canvas")
    draw_image("canvas", img_file_name, [0, 0], pmax=[img_size_x, img_size_y])


def show_route(sender, callback):
    '''Display a map image for the destination coordinates'''
    coords1 = get_value("Coords")
    coords2 = get_value("destination_text")
    get_route_image(coords1, coords2)

    # update canvas
    clear_drawing("canvas")
    draw_image("canvas", img_file_name, [0, 0], pmax=[img_size_x, img_size_y])


def get_random_destination(sender, callback):
    '''Get new random destination based on starting coordinates'''
    coords = get_value("Coords")

    # calculate new coords and write then in the destination text box
    coord_list = coords.split(',')
    latitude = float(coord_list[0])
    longitude = float(coord_list[1])
    new_coords = get_random_location(latitude, longitude, MAX_DIST)
    new_coords_str = f"{str(new_coords[0])},{str(new_coords[1])}"
    set_value("destination_text", new_coords_str)


def main():
    '''main routine to draw the UI and start the GUI'''
    global maps_key
    load_dotenv()
    maps_key = os.environ.get("BING_MAPS_KEY")
    coords = os.environ.get("DEFAULT_COORDS")

    # set main window defaults
    set_main_window_size(img_size_x + 20, img_size_y + 90)
    set_main_window_pos(100, 25)
    set_main_window_title("Map image utility")

    with window("Main"):
        add_text("Coordinates: ")
        add_same_line()
        add_input_text("Coords", label="", default_value=coords, width=170, callback=show_origin, on_enter=True)
        add_same_line()
        add_button("Show origin", callback=show_origin)
        add_text("Destination: ")
        add_same_line()
        add_input_text("destination_text", label="", width=170)
        add_same_line()
        add_button("Random destination", callback=get_random_destination)
        add_same_line()
        add_button("Show destination", callback=show_destination)
        add_same_line()
        add_button("Show route", callback=show_route)
        add_text("bearing_label", default_value=" ")
        add_spacing()
        add_separator()
        add_spacing()
        add_drawing("canvas", width=img_size_x, height=img_size_y)
        #if os.path.isfile(img_file_name):
        #    draw_image("canvas", img_file_name, [0, 0], pmax=[img_size_x, img_size_y])

    start_dearpygui(primary_window="Main")


if __name__ == "__main__":
    main()
