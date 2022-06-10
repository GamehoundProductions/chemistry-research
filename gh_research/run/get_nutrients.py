#!/usr/bin/python3
import argparse
import os
import json

from gh_research.api.fdc.fdc_food import FDCFood
from gh_research.api.utils import nutrients_from_data


def _get_data_from_file(path: str):
    if not os.path.exists(path): return None
    if not os.path.isfile(path): return None

    content = None
    with open(path, 'r+') as file_obj:
        content = file_obj.read()
    content = json.loads(content)
    return content


def main(args):
    id = ''
    file_data = _get_data_from_file(args['id'])
    data_as_json = None
    if file_data is not None:
        id = file_data.get('fdcId')

    if not id:
        raise ValueError('fdcId not found in the json file "%s"' % args['id'])

    Food = FDCFood(id, api_key=args['api_key'])

    if file_data:
        # data = Food.get_nutrients()
        data = Food.process_nutrients_data(file_data)
        # data = { 'id' : id }
        # data['nutrients'] = nutrients_from_data(file_data)
        data_as_json = json.dumps(data)
    else:
        data = Food.get_nutrients()
        data_as_json = json.dumps(data.json())

    print(data_as_json)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--id',
                        help='ID or a file path of the food item to get data for.',
                        required=True)
    parser.add_argument('--api-key', '-k',
                        help='Api key file or string',
                        required=True)

    args = parser.parse_args()
    main(vars(args))
