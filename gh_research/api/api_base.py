from abc import ABCMeta, abstractmethod
import os
import requests
from urllib.parse import urljoin


class APIBase(metaclass=ABCMeta):

    def __init__(self, **kwargs):
        self.api_key = kwargs.get('api_key', None)
        if (self.api_key and os.path.isfile(self.api_key)):
            self.api_key = self.parse_api_key(self.api_key)

        self.limit = 5
        self.HTTP = requests.Session()


    def GET(self) -> requests.Response:
        return self.HTTP.get(self.url)


    @property
    def url(self) -> str:
        url = urljoin(self.base_url, self.endpoint,)
        api_key = '&api_key=%s' % self.api_key if self.api_key else ''
        return '%s%s%s' % (url, self.query, api_key)


    @property
    def base_url(self) -> str:
        return 'https://api.nal.usda.gov/'


    @property
    @abstractmethod
    def endpoint(self) -> str:
        ...


    @property
    @abstractmethod
    def query(self) -> str:
        ...


    def _set_requests_session(session: requests.Session):
        session.headers.update({
            'Accept':' application/json',
        })

    def parse_api_key(self, api_file):
        if not os.path.exists(api_file):
            return api_file

        file_data = None
        with open(api_file, 'r') as file_obj:
            file_data = file_obj.read()

        return file_data.split('\n')[0]


    def search_by_name(self, whatToSearch):
        endpoint = '?format=json&offset=0&sort=n&q={target}&max={limit}&api_key={key}'
        endpoint = endpoint.format(target=whatToSearch,
                            key=self.api_key,
                            limit=self.limit)

        url = self.search_url + endpoint
        response = self.HTTP.get(url)
        return response.json()


    def search_by_id(self, id):
        '''
            @return: { nutrients: [ { derivation, group, measures, name,
                                      nutrient_id, unit, value} ] }
        '''
        endpoint = '{id}?format=full&nutrients=203&nutrients=204&nutrients=205&api_key={api_key}'
        endpoint = endpoint.format(id=id, api_key=self.api_key)

        url = self.food_url + endpoint
        response = self.HTTP.get(url)
        return response.json()


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
