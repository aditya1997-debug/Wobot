from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

client = MongoClient("mongodb+srv://Aditya_fcc:manutd10@freecodecamp.imwlexe.mongodb.net/?retryWrites=true&w=majority&appName=FreeCodeCamp", server_api=ServerApi('1'))

db = client.todolist_db

task_collection = db["Todo List"]
users_collection = db["Users"]