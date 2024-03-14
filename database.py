from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json
from bson import ObjectId
from random import randint

class Database:
    def __init__(self):
        key = json.load(open("key.json"))
        uri = "mongodb+srv://elianrenteria:"+key["password"]+"@cluster0.jzllzcw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        # Create a new client and connect to the server
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        # Send a ping to confirm a successful connection
        try:
            self.client.admin.command('ping')
            #print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

    def check_user_exists(self, username):
        db = self.client["Wander"]
        collection = db["users"]
        user = collection.find_one({"username": username})
        if user:
            return True
        return False

    def create_user(self, username, password):
        db = self.client["Wander"]
        collection = db["users"]
        new_id = ObjectId()
        user = {"_id": new_id, "username": username, "password": password, "color":{"red": randint(0,255), "green": randint(0, 255), "blue": randint(0, 255)}}
        collection.insert_one(user)
        if self.check_user_exists(username):
            print(f"User created successfully! {new_id}")
        else:
            print("User not created")
            self.create_user(username, password)

    def check_password(self, username, password):
        db = self.client["Wander"]
        collection = db["users"]
        user = collection.find_one({"username": username, "password": password})
        if user:
            return True
        return False

    def get_user(self, username):
        db = self.client["Wander"]
        collection = db["users"]
        user = collection.find_one({"username": username})
        print(user)
        return user

    def close(self):
        self.client.close()

#Testdb = Database()
#Testdb.get_user("Elian")
# print(db.check_user_exists("Elian"))
# print(db.create_user("elian", "123"))
# print(db.check_password("elian", "123"))
# db.close()
#Testdb.create_user("Charlie", "poop123")