import os
from dotenv import load_dotenv, dotenv_values
import pymongo
from pymongo import MongoClient
import urllib
from bson.objectid import ObjectId

load_dotenv()


class database:
    client = MongoClient()
    
    def __init__(self):
        uri = f"mongodb+srv://{urllib.parse.quote(os.getenv("USERNAME"))}:{urllib.parse.quote(os.getenv("PASSWORD"))}@cluster0.laxqhrx.mongodb.net/?appName=Cluster0"

        try:
            self.client = MongoClient(uri)

            database = self.client["minecraft-scan"]
            self.collection = database["Cluster0"]
            print("Connected in MongoDb!")
        except Exception as e:
            raise Exception( "The fallowing error occurred: ", e)
        
    def create(self, IP:str, PORT:int):
        payload = {"ip":IP, "port":str(PORT)}
        result = self.collection.insert_one(payload)
        print(result.acknowledged)
    
    def delete(self, id):
        query_filter = { "_id" : ObjectId(f"{id}") }
        print(query_filter)
        result = self.collection.delete_one(query_filter)
        print(result.deleted_count)

    def select(self):
        list = []
        result = self.collection.find({})

        for x in result:
            list.append(x)
        return list
    
    def __delattr__(self):
        self.client.close()