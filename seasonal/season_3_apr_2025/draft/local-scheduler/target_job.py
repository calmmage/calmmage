"""
Sample task

- idea 1: just hello world
- idea 2: connect to a local mongodb and write something to a test collection
- idea 3: test something meaningful - for example, connect to a llm using env vars
"""
import os
import datetime
from pathlib import Path
import pymongo
from pymongo import MongoClient

def run_hello_world():
    print("Hello world")

test_database = "local"
test_colecction = "test_local_scheduler"

client = MongoClient("mongodb://localhost:27017/")
db = client[test_database]
collection = db[test_colecction]

def run_mongodb():
    value = os.getenv("SAMPLE_JOB_SOURCE", "run as main")
    # Insert a document
    test_document = {"name": "target_job",
                     "filepath":__file__,
                     "value":value,
                     "timestamp": datetime.datetime.now()}
    collection.insert_one(test_document)

    # Retrieve the document
    retrieved_document = collection.find_one({"name": test_document['name']})
    print(retrieved_document)

def run_env_access():

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")



if __name__ == '__main__':
    # run the test task
    # run_hello_world()
    run_mongodb()
    # print(1)