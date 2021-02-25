import pymongo
import yaml

config = yaml.load(open('config.yml'), Loader=yaml.FullLoader).get('mongo')


class DatabaseConnector:
    client = None
    db = None
    collection = None

    def __init__(self):
        self.client = pymongo.MongoClient(config.get('host'), config.get('port'))
        self.db = self.client['frExtensionDB']
        self.collection = self.db['sample_data']

    def insert(self, data):
        self.collection.insert_one(data)

    def get(self, guid):
        return self.collection.find({'guid': guid})

    def count(self, guid):
        return self.collection.count_documents({'guid': guid})
