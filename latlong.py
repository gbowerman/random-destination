'''Random destination'''
import math
import random
import sys

EARTH_RADIUS = 6378.1
MIN_DIST = 1
MAX_DIST = 16 # destination radius in KM

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
    print(f"Bearing: {str(bearing)}, Distance (km): {str(distance_km)}")
    
    # calculate the new latitude and longitude
    return plot_location(latitude, longitude, bearing, distance_km)


def main():
    '''Get a location and find a random destination within 10 miles'''
    if len(sys.argv) != 2:
        exit("Expecting a lat,lon argument on command line")
    coord_list = sys.argv[1].split(',')
    latitude = float(coord_list[0])
    longitude = float(coord_list[1])

    new_coords = get_random_location(latitude, longitude, MAX_DIST)
    print(f"New coords: {str(new_coords[0])},{str(new_coords[1])}")

if __name__ == "__main__":
    main()