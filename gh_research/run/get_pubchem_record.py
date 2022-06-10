#!/usr/bin/python3
import argparse
import json

from gh_research.api.pubchem.pubchem_record import PubchemRecord


def main(args):
    id = args['id']
    PubchemItem = PubchemRecord(id)

    data = PubchemItem.GET()
    print(data.url)
    data_as_json = json.dumps(data.json())
    print(data_as_json)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--id',
                        help='CID of the record to get the data of.',
                        required=True)

    args = parser.parse_args()
    main(vars(args))
