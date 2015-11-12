import pymongo

MONGODB_URI = 'mongodb://emeril:lagasse@ds053964.mongolab.com:53964/pantry'

SEED_DATA = [
    {
        'name': 'Quesadilla',
        'ingredients': [
            'tortilla',
            'cheese'
        ]
    },
    {
        'name': 'Grilled Cheese',
        'ingredients': [
            'bread',
            'cheese'
        ]
    },
]

def seed_db():
    adapter = DatabaseAdapter()
    adapter.add_recipe('Grilled Cheese', ['bread', 'cheese'])
    adapter.add_recipe('Quesadilla', ['tortilla', 'cheese'])

class DatabaseAdapter():

    def __init__(self):
        self.client = pymongo.MongoClient(MONGODB_URI)
        self.db = self.client.get_default_database()

    def add_recipe(self, name, ingredients):
        self.db['recipes'].insert({'name': name, 'ingredient': ingredients})

if __name__ == '__main__':
    seed_db()
