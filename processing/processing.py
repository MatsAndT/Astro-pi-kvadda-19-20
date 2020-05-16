import argparse

def main(folder, db):
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some iss data.')
    parser.add_argument('pictures', type=str,
                        help='path where the pictures are')
    parser.add_argument('db', dest='accumulate', type=str, help='path to db')

    args = parser.parse_args()

    main(args.fodler, args.db)