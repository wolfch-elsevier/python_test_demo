import pprint
import re
import sys
from pprint import pprint
from urllib.parse import quote_plus
from bson.objectid import ObjectId
from pymongo import MongoClient

MDB_MASTER_IP = "10.149.154.237"
MDB_NODE1_IP = "10.149.154.191"
MDB_NODE2_IP = "10.149.154.235"
MDB_USER = "stanRootAdmin"
MDB_PASS = "8zBlmA2GOn"

# DEV_URL=f"mongodb://{MDB_USER}:{MDB_PASS}@{MDB_MASTER_IP}:27017,{MDB_NODE1_IP}:27017,{MDB_NODE2_IP}:27017/admin?replicaSet=HGRAPH_STAN_PROD"
DEV_URL = f"mongodb://{MDB_USER}:{MDB_PASS}@localhost:27018"


class WebprotegeDB:
    def __init__(
        self,
        mongo_url=None,
        mongo_client=None,
        host=None,
        port=None,
        username=None,
        password=None,
        mongo_db="webprotege",
    ) -> None:
        # if not mongo_url and not mongo_client:
        #    raise Exception("must pass either mongo_url or mongo_client instance")
        self.mclient = (
            mongo_client
            if mongo_client
            else MongoClient(host=host, port=port, username=username, password=password)
        )
        self.webprotege_db = self.mclient[mongo_db]

    def add_record(self, collection_name, record):
        return str(self.webprotege_db[collection_name].insert_one(record).inserted_id)

    def update_record(self, collection_name, record):
        return self.webprotege_db[collection_name].update_one(
            {"_id": record["_id"]}, {"$set": record}, upsert=False
        )

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
    # MDB_URL="mongodb://stanRootAdmin:8zBlmA2GOn@10.149.154.237:27017"
    MDB_URL = "mongodb://localhost:27017/"
    db = WebprotegeDB(MDB_URL, mongo_db="webprotege")
    # db = WebprotegeDB(host="localhost", port=27018, username="stanRootAdmin", password="8zBlmA2GOn", mongo_db="webprotege")
    # role_record = db.fetch_record_by_query("RoleAssignments", {"userName": "stanAdmin"})
    record = db.fetch_record_by_query("ProjectDetails", {"owner": "stanAdmin"})
    record["defaultDisplayNameSettings"]["primaryDisplayNameLanguages"] = []
    """
    for display_name_language in record["defaultDisplayNameSettings"]["primaryDisplayNameLanguages"]:
        if "lang" not in display_name_language or not display_name_language["lang"]:
            display_name_language["lang"] = "en"
    """
    # pprint(record)
    db.update_record("ProjectDetails", record)
    # for record in db.find_all_records("ProjectDetails"):
    #    print(record)

    """
    for role in role_record["roleClosure"]:
        if role not in role_record["assignedRoles"]:
            role_record["assignedRoles"].append(role)
    """

    sys.exit(0)
    for record in db.find_all_records("Users"):
        print(f"{record['_id']}: {record['realName']}")
