import argparse
from database import DataBase
from time_to_position import TimeToLatLon

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some iss data.')
    parser.add_argument('pictures', type=str,
                        help='path where the pictures are')
    parser.add_argument('db', dest='accumulate', type=str, help='path to db')

    args = parser.parse_args()

    main(args.fodler, args.db)