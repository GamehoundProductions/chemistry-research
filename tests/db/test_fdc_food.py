#!/usr/bin/python3
from sqlalchemy import true
from urllib.parse import urljoin
import unittest
from pdb import set_trace

from gh_research.api import FDCFood


class FDCFoodTests(unittest.TestCase):

    id = 1
    api_key = '123'
    base_url = 'https://api.nal.usda.gov/'


    def setUp(self) -> None:
        self.endpoint = 'fdc/v1/food/{}'.format(self.id)
        self.query = '?format=full'
        self.url = 'https://api.nal.usda.gov/fdc/v1/food/1' + \
            self.query + \
            '&api_key=%s' % self.api_key

        self.Food = FDCFood(self.api_key, self.id)


    def test_constructor(self):
        self.assertEqual(self.Food.api_key, self.api_key)
        self.assertEqual(self.Food.id, self.id)


    def test_url(self):
        self.assertEqual(self.Food.endpoint, self.endpoint)
        self.assertEqual(self.Food.base_url, self.base_url)
        self.assertEqual(self.Food.query, self.query)
        self.assertEqual(self.Food.url, self.url)


if __name__ == '__main__':
    unittest.main()
