import argparse
from data import Data
from time_to_position import TimeToLatLon
import requests
import json
import reverse_geocoder as rg

time_zone = '+0000'


def main(folder, db, row_length, csv_path):
    data_handler = Data(db, csv_path)
    data_handler.add_column()
    ttp = TimeToLatLon()

    for i in range(row_length):
        print(f'processing row {i}')
        row = data_handler.next()
        # row[1] is the time
        lat, lon = ttp.convert(row[1]+time_zone)
        print(f'lat: {lat}, lon: {lon}')
        name, region, country = getplace(lat, lon)
        print(f'name: {name}, region: {region}, country: {country}')
        co2 = data_handler.get_co2(country)
        print(f'co2: {co2}')
        
        # row[0] is the id
        data_handler.add_data(row[0], name, region, country, co2, lat, lon)
        print('added new data to database')
        print('\n\n')

    data_handler.close_conn()
    ttp.quit()

# https://stackoverflow.com/a/20169528/7419883
def getplace(lat, lon):
    ''' Convert lat and lon to a place on the map with town and country '''
    results = rg.search((lat, lon))[0]
    code = results['cc']
    name = results['name']
    region = results['admin1']

    try:
        res = requests.get('https://restcountries.eu/rest/v2/alpha/'+code)
        country = res.json()['name']
    except:
        print('Did not get country name')
        country = ''
    
    return name, region, country

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some iss data.')
    parser.add_argument('pictures', type=str,
                        help='path where the pictures are')
    parser.add_argument('db', type=str, help='path to db')
    parser.add_argument('row_length', help='row length', type=int)
    parser.add_argument('csv_path', help='path for co2 data', type=str)
    args = parser.parse_args()

    main(args.pictures, args.db, args.row_length, args.csv_path)

# python processing.py ../data/ ../data/teamkvadda_data_database.sqlite 709 ../data/co2_2018.csv
