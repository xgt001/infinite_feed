from ConfigParser import SafeConfigParser
import ConfigParser
from pymongo import MongoClient

class MongoDoc(object):
    def __init__(self):
        self.client = self.__create_client()
  
    def read_properties(self, setting_type, setting):
        parser = SafeConfigParser()
        try:
            parser.read("social_media.config")
            return parser.get(setting_type, setting)
        except (ConfigParser.ParsingError, ConfigParser.NoSectionError) as err:
            print "Error while reading mongo settings from file. {}".format(err)

    def __create_client(self):
        host = self.read_properties("mongo", "host")
        db_name = self.read_properties("mongo", "database")
        try:
            client = MongoClient(host, 9000)
            db_conn = client[db_name]
            return db_conn
        except pymongo.errors.ConnectionFailure as err:
            print "Error connecting to Mongo host {}. {}".format(host, err)

class MongoOP(MongoDoc):
    def store_values(self, feed):
        db_conn = self.client
        collection = self.read_properties("mongo", "collection")
        try:
            db_conn = db_conn[collection]
            db_conn.insert_one(feed)
        except (pymongo.errors.WriteError, pymongo.errors.CollectionInvalid) as err:
            print "Error writing value {} to collection {}. {}".format(feed, collection, err)
