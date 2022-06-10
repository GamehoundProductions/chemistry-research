from pprint import pprint

from gh_research.api.api_base import APIBase


class PubchemCIDS(APIBase):

    def __init__(self, id, **kwargs):
        super().__init__(**kwargs)
        self.id = id


    @property
    def endpoint(self):
        return 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/'


    @property
    def query(self) -> str:
        return '/name/%s/cids/json?name_type=word' % self.id
