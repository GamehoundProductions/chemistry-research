#!/usr/bin/python3
import argparse
import json

from gh_research.api.pubchem.pubchem_cids import PubchemCIDS


def main(args):
    id = args['id']
    Food = PubchemCIDS(id)

    data = Food.GET()
    data_as_json = json.dumps(data.json())
    print(data_as_json)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--id',
                        help='Name of the compound to get list of CIDS of.',
                        required=True)

    args = parser.parse_args()
    main(vars(args))
