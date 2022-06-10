from typing import TypedDict


class NutrientItem(TypedDict):
    id: str
    number: str
    name: str
    rank: int
    unitName: str
    amount: float
    type: str


class NutrientCollection(TypedDict):
    proximates: list[NutrientItem]
    carbohydrates: list[NutrientItem]
    minerals: list[NutrientItem]
    other: list[NutrientItem]
    excluded: list[NutrientItem]


class NutrientsData(TypedDict):
    id: str
    nutrients: NutrientCollection
