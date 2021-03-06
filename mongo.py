import os
import pymongo
if os.path.exists("env.py"):
    import env

MONGO_URI = os.environ.get("MONGO_URI")
DATABASE = "myFirstDB"
COLLECTION = "celebrities"

# Function to grab db data from MongoDB

def mongo_connect(url):
    try:
        conn = pymongo.MongoClient(url)
        print("Mongo is connected")
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print("Couldn't connect to MongoDB: %s") % e

conn = mongo_connect(MONGO_URI)

coll = conn[DATABASE][COLLECTION]

# coll.update_many({"nationality": "british"}, {"$set": {"hair_color": "teal"}})

documents = coll.find()

for doc in documents:
    print(doc)