from pprint import pprint

from gh_research.api.api_base import APIBase
from ..utils import nutrients_from_data
from gh_research.typing.type_nutrients import NutrientCollection, NutrientsData, NutrientItem


class FDCFood(APIBase):

    def __init__(self, id, **kwargs):
        super().__init__(**kwargs)
        self.id = id


    def get_nutrients(self) -> NutrientsData:
        resp = self.GET()
        if resp.status_code != 200: return {}
        data = resp.json()
        return self.process_nutrients_data(data)


    def process_nutrients_data(self, data: NutrientCollection) -> NutrientsData:
        nutrients: NutrientCollection = nutrients_from_data(data)
        if not nutrients.get('excluded'):
            nutrients['excluded'] = []
        # nutrients['proximates'] = list(filter(self.filter_none_chemicals, nutrients['proximates']))
        for category in self.categories:
            proximatessFilters = self.filter_none_chemicals(nutrients.get(category))
            nutrients[category] = proximatessFilters['items']
            nutrients['excluded'].extend(proximatessFilters['filtered'])

        return {
            'id' : self.id,
            'nutrients' : nutrients
        }


    def filter_none_chemicals(self, items: list[NutrientItem]):
        if not items: return

        exclude_names = [
            'Energy (Atwater General Factors)',
            'Energy (Atwater Specific Factors)',
            'Carbohydrate, by difference',
            'Carbohydrate, by summation',
            'Fiber, total dietary'
            ]
        filtered: list[NutrientItem] = []
        result: list[NutrientItem] = []
        for item in items:
            if item['name'] in exclude_names:
                filtered.append(item)
            else:
                result.append(item)
        return { 'items': result, 'filtered': filtered }


    @property
    def endpoint(self):
        return 'fdc/v1/food/{0}'.format(self.id)


    @property
    def query(self) -> str:
        return '?format=full'


    @property
    def categories(self) -> list[str]:
        return ['proximates', 'carbohydrates', 'minerals', 'other']
