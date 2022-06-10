from gh_research.typing.type_nutrients import NutrientCollection

'''
 Return an object of chemical elements containing in the fdcID item.

 @param data: an FDC response's "foodNutrients" parsed object into the following
            format:
            { "id": int,
                "nutrient": {
                    "proximates" : [],
                    "carbohydrates": [],
                    "minerals": [],
                    "other": [],
                }
            }
'''
def nutrients_from_data(data: object) -> NutrientCollection:
    items: NutrientCollection = {}
    item_type = ''

    for nutrient in data['foodNutrients']:
        item = nutrient.get('nutrient')
        amount = nutrient.get('amount')

        if not item: continue

        if is_nutrient_title(nutrient):
            item_type = item['name'].lower()
            if item_type == 'vitamins and other components':
                item_type = 'other'
            if not items.get(item_type):
                items[item_type] = []

        if not amount: continue

        item['amount'] = amount
        item['type'] = item_type
        items[item_type].append(item)
    return items


def is_nutrient_title(item: object):
    keys = list(item.keys())
    return keys == ['nutrient', 'type']
