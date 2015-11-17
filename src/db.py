import pymongo
from itertools import permutations
import random
import numpy as np

MONGODB_URI = 'mongodb://emeril:lagasse@ds053964.mongolab.com:53964/pantry'
AVERAGE_INGREDIENT_COUNT = 10

def pairs_string(ingredients):
    return ','.join([a.replace(' ', '_') + '+' + b.replace(' ', '_') for a, b in permutations(ingredients, 2)])

def random_recipes(count):
    ingredients = all_ingredients()
    for i in range(count):
        yield pairs_string(random.sample(ingredients, AVERAGE_INGREDIENT_COUNT))

def all_recipes_pairs():
    return [pairs_string(recipe) for recipe in DatabaseAdapter().all_recipes()]

def all_ingredients():
    return set([ingredient for recipe in DatabaseAdapter().all_recipes() for ingredient in recipe])

class DatabaseAdapter():

    def __init__(self):
        self.client = pymongo.MongoClient(MONGODB_URI)
        self.db = self.client.get_default_database()

    def add_recipe(self, name, ingredients):
        self.db['recipes'].insert({'name': name, 'ingredient': ingredients})

    def all_recipes(self):
        return filter(len, [recipe['ingredient'] for recipe in self.db['recipes'].find()])

    def __del__(self):
        self.client.close()

if __name__ == '__main__':
    pass
