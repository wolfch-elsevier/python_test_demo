import pprint
import re
import sys

from bson.objectid import ObjectId
from pymongo import MongoClient


class SubscriberData:
    def __init__(self, mongo_url=None, mongo_client=None) -> None:
        if not mongo_url and not mongo_client:
            raise Exception("must pass either mongo_url or mongo_client instance")
        self.mclient = mongo_client if mongo_client else MongoClient(mongo_url)
        self.subscriber_db = self.mclient.subscriber_db
        self.usa = self.subscriber_db.usa
        
    def add_subscriber(self, subscriber_geo_zone, subscriber_record):
        return str(self.subscriber_db[subscriber_geo_zone].insert_one(subscriber_record).inserted_id)
    
    def delete_subscriber(self, subscriber_geo_zone, id):
        result = self.subscriber_db[subscriber_geo_zone].delete_one({"_id": ObjectId(id)})
        return result.deleted_count
    
    def delete_subscribers(self, subscriber_geo_zone, ids):
        ct = 0
        for id in ids:
            ct += self.delete_subscriber(subscriber_geo_zone, id)
        return ct
        
    def fetch_subscriber_by_id(self, subscriber_geo_zone, id):
        return self.subscriber_db[subscriber_geo_zone].find_one({"_id": ObjectId(id)})
    
    def fetch_record_by_query(self, collection_name, query):
        return self.subscriber_db[collection_name].find_one(query)
    
    def find_all_subscribers(self, subscriber_geo_zone):
        # convert Cursor traversal into records generator
        for subscriber in self.subscriber_db[subscriber_geo_zone].find():
            yield subscriber
    
    def close(self):
        if self.mclient:
            self.mclient.close()
 
