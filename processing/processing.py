import argparse
from database import DataBase
from time_to_position import TimeToLatLon

from urllib import urlopen
import json

db_path = '../data/teamkvadda_data_database.sqlite'
time_zone = '+0000'

def main(folder, db):
    db_handeler = DataBase(db_path)
    ttp = TimeToLatLon()

    while True:
        row = db_handeler.next()
        lat, lon = ttp.convert(row['time']+time_zone)

        address = to_address(lat, lon)
        town, country = getplace(lat, lon)

### https://stackoverflow.com/a/20169528/7419883
def getplace(lat, lon):
    url = "http://maps.googleapis.com/maps/api/geocode/json?"
    url += "latlng=%s,%s&sensor=false" % (lat, lon)
    v = urlopen(url).read()
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
    parser.add_argument('db', dest='accumulate', type=str, help='path to db')
    args = parser.parse_args()

    main(args.fodler, args.db)
