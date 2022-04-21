import pprint
import re
import sys

from bson.objectid import ObjectId
from pymongo import MongoClient


class WebprotegeDB:
    def __init__(self, mongo_url=None, mongo_client=None, mongo_db="webprotege") -> None:
        if not mongo_url and not mongo_client:
            raise Exception("must pass either mongo_url or mongo_client instance")
        self.mclient = mongo_client if mongo_client else MongoClient(mongo_url)
        self.webprotege_db = self.mclient[mongo_db]
        
    def add_record(self, collection_name, record):
        return str(self.webprotege_db[collection_name].insert_one(record).inserted_id)
    
    def delete_record(self, collection_name, id):
        result = self.webprotege_db[collection_name].delete_one({"_id": ObjectId(id)})
        return result.deleted_count
    
    def delete_records(self, collection_name, ids):
        ct = 0
        for id in ids:
            ct += self.delete_record(collection_name, id)
        return ct
        
    def fetch_record_by_id(self, collection_name, id):
        return self.webprotege_db[collection_name].find_one({"_id": ObjectId(id)})
    
    def fetch_record_by_query(self, collection_name, query):
        return self.webprotege_db[collection_name].find_one(query)
    
    def find_all_records(self, collection_name):
        # convert Cursor traversal into records generator
        for record in self.webprotege_db[collection_name].find():
            yield record
    
    def close(self):
        if self.mclient:
            self.mclient.close()
 
if __name__ == "__main__":
    # MDB_URI="mongodb://3.238.5.250:27017/"
    MDB_URI="mongodb://localhost:27017/"
    db = WebprotegeDB(MDB_URI, mongo_db="webprotege")
    role_record = db.fetch_record_by_query("RoleAssignments", {"userName": "stanAdmin"})
    for role in role_record["roleClosure"]:
        if role not in role_record["assignedRoles"]:
            role_record["assignedRoles"].append(role)
    db.
            
    sys.exit(0)
    for record in db.find_all_records("Users"):
         print(f"{record['_id']}: {record['realName']}")
