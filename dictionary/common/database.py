import pymongo


class Database(object):
    URI = 'mongodb://127.0.0.1:27017'
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['dictionary']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def bulk_write(collection, operations):
        Database.DATABASE[collection].bulk_write(operations)

    @staticmethod
    def insert_many(collection, data_json_list):
        Database.DATABASE[collection].insert_many(data_json_list)

    @staticmethod
    def find(collection, data):
        return Database.DATABASE[collection].find(data)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)
