#!/usr/bin/python3
import argparse
import os
import requests
from pprint import pprint
from pdb import set_trace


class Searcher:

    def __init__(self, api_key):
        self.search_url = 'https://api.nal.usda.gov/ndb/search/'
        self.food_url = 'https://api.nal.usda.gov/ndb/reports/'

        self.api_key = self.parse_api(api_key)
        self.limit = 5


    def parse_api(self, api_file):
        if not os.path.exists(api_file):
            return api_file

        file_data = None
        with open(api_file, 'r') as file_obj:
            file_data = file_obj.read()

        return file_data.split('\n')[0]


    def search_by_name(self, whatToSearch):
        endpoint = '?format=json&offset=0&sort=n&q={target}&max={limit}&api_key={key}'\
                    .format(target=whatToSearch,
                            key=self.api_key,
                            limit=self.limit)

        response = requests.get(self.search_url + endpoint)
        return response.json()['list']


    def search_by_ndbno(self, ndbno):
        '''
            @return: { nutrients: [ { derivation, group, measures, name,
                                      nutrient_id, unit, value} ] }
        '''
        endpoint = '?ndbno={ndbno}&type=b&format=json&api_key={api_key}'\
                    .format(ndbno=ndbno,api_key=self.api_key)

        response = requests.get(self.food_url + endpoint)
        return response.json()['report']['food']


    def get_minerals_from_data(self, data):
        '''
            @param data: [ {group, measures, name, nutrient_id, unit, value, derivation} ]
        '''
        minerals = []
        for nutrient in data:
            if nutrient['group'] != 'Minerals':
                continue
            minerals.append(nutrient)

        return minerals


    def get_chemical_element(self, minerals):
        '''
            @param minerals: something returned by get_minerals_from_data
        '''
        result = []
        for data in minerals:
            mineral_name = data.get('name', None)
            if mineral_name is not None:
                result.append(mineral_name)
        return result


    def get_ndbno(self, data):
        '''
        @param data: [{ ds, group, menu, name, ndbno, offset }]
        '''
        ndbnoList = [foodInfo['ndbno'] for foodInfo in data]
        return ndbnoList


def main(args):
    toSearch = args['name']
    searcher = Searcher(args['api_key'])

    search_result = searcher.search_by_name(toSearch)
    #pprint(search_result)

    ndbnoList = searcher.get_ndbno(search_result['item'])
    food_info = searcher.search_by_ndbno(ndbnoList[0])
    minerals = searcher.get_minerals_from_data(food_info['nutrients'])
    chemicals = searcher.get_chemical_element(minerals)
    pprint(chemicals)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', '-n',
                        help='What to search')
    parser.add_argument('--api-key', '-k',
                        help='Api key file or string')

    args = parser.parse_args()
    main(vars(args))
