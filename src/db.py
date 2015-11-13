import pymongo

MONGODB_URI = 'mongodb://emeril:lagasse@ds053964.mongolab.com:53964/pantry'

class DatabaseAdapter():

    def __init__(self):
        self.client = pymongo.MongoClient(MONGODB_URI)
        self.db = self.client.get_default_database()

    def add_recipe(self, name, ingredients):
        self.db['recipes'].insert({'name': name, 'ingredient': ingredients})

    def __del__(self):
        self.client.close()

if __name__ == '__main__':
    seed_db()
