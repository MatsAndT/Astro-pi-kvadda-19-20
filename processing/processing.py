import argparse
from data import Data
from time_to_position import TimeToLatLon

import requests
import json

time_zone = '+0000'

def main(folder, db, row_length, csv_path):
    data_handeler = Data(db, csv_path)
    data_handeler.add_colum()
    ttp = TimeToLatLon()

    for i in range(row_length):
        print('processing row %x' % i)
        row = data_handeler.next()
        lat, lon = ttp.convert(row['time']+time_zone)
        print('lat: %s, lon: %s' % (lat, lon))
        town, country = getplace(lat, lon)
        print('town: %s, country: %s' % (town, country))
        co2 = data_handeler.get_co2(country)
        print('co2: %s' % co2)
        
        data_handeler.add_data(row['id'], town, country, co2, lat, lon)
        print('added new data to database')
        print('\n\n')

    data_handeler.close_conn()
    ttp.quit()


### https://stackoverflow.com/a/20169528/7419883
def getplace(lat, lon):
    '''
    Convert lat and lon to a place on the map with town and country
    '''
    url = "http://maps.googleapis.com/maps/api/geocode/json?"
    url += "latlng=%s,%s&sensor=false" % (lat, lon)
    v = requests.get(url)
    j = json.loads(v)
    components = j['results'][0]['address_components']
    country = town = None
    for c in components:
        if "country" in c['types']:
            country = c['long_name']
        if "postal_town" in c['types']:
            town = c['long_name']
    return town, country

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some iss data.')
    parser.add_argument('pictures', type=str,
                        help='path where the pictures are')
    parser.add_argument('db', type=str, help='path to db')
    parser.add_argument('row_length', help='row length', type=int)
    parser.add_argument('csv_path', help='path for co2 data', type=str)
    args = parser.parse_args()

    main(args.fodler, args.db, args.row_lenght, args.csv_path)
