#-----------------------------------------------------------------------
# distance_func.py
# This file contains functions relating distance calculation
#-----------------------------------------------------------------------
import psycopg2
from geopy.distance import geodesic

#-----------------------------------------------------------------------

DATABASE_URL = 'postgresql://tigerspot_database_990e_user:s5cZDU5NrHEaLniMWf2C4L2kzOIxigFZ@dpg-cruv9ig8fa8c73cobdog-a.ohio-postgres.render.com/tigerspot_database_990e'
# DATABASE_URL = 'postgresql://tigerspot_database_user:uzR6eRWos4EgeX39bk3kAY7akdrfmV2O@dpg-cre8kjbgbbvc73bos7v0-a.ohio-postgres.render.com/tigerspot_database'

#-----------------------------------------------------------------------

#Using the geopy library, we calculate the distance between two coordinates using the Haversine formula
#Measuring in meters
def calc_distance(lat1, lon1, coor2):
    coor1 = (lat1, lon1)
    distance = geodesic(coor1, coor2).meters
    return round(distance)

#-----------------------------------------------------------------------
def testing():
    #testing that calc_distance() calculates correct distance
    expected_distance = 751 #estimation using calculator
    calculated_distance = calc_distance(40.3487 , -74.6593, (40.3421, -74.6612))
    print("Expected distance:", expected_distance)
    print("Calculated distance:", calculated_distance)

    if(abs(expected_distance - calculated_distance) > 2):
        print("Error with distance calculation")

    expected_distance = 474
    calculated_distance = calc_distance(40.340709282911774, -74.66445011628363, (40.34184596123739,-74.65906424092816))
    print("Expected distance:", expected_distance)
    print("Calculated distance:", calculated_distance)

    if(abs(expected_distance - calculated_distance) > 2):
        print("Error with distance calculation")

#-----------------------------------------------------------------------

def main():
    testing()
    
if __name__=="__main__":
    main()