import pymongo

client = pymongo.MongoClient('localhost', 27017)
db = client['frExDB']
col = db['sample_data']

print(db.list_collection_names())
