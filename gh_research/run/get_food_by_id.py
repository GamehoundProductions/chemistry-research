#!/usr/bin/python3
import argparse
import json

from gh_research.api.fdc.fdc_food import FDCFood


def main(args):
    id = args['id']
    Food = FDCFood(id, api_key=args['api_key'])

    data = Food.GET()
    data_as_json = json.dumps(data.json())
    print(data_as_json)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--id',
                        help='ID of the food item to get data for.',
                        required=True)
    parser.add_argument('--api-key', '-k',
                        help='Api key file or string',
                        required=True)

    args = parser.parse_args()
    main(vars(args))
