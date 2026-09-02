import os
import sys
import json

from dotenv import load_dotenv
load_dotenv()

# then access your variables like:
MONGO_DB_URL = os.getenv("MONGODB_URI")
print(MONGO_DB_URL)

import certifi ## it is a python package that provide a set of root ceetificate, used to make a Secure HTTP connection 
ca=certifi.where()

import pandas as pd
import numpy as np
import pymongo

from networkSecurity.exception.exception import NetworkSecurityException
from networkSecurity.logging.logger import logger


class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def csv_to_json_conversion(self,file_path):
        try:
            data=pd.read_csv(file_path)
            ## Dropping the index
            data.reset_index(drop=True,inplace=True)
            ## 1. transposing the data
            ## 2. Converting the data into JSON
            ## 3. Making the list of JSON
            records=list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys) 


    def insert_data_to_mongoDb(self,records,database,collection):
        try:

            ##Stores the passed arguments as instance variables so they can be used throughout the method.
            self.database=database
            self.collection=collection
            self.records=records

            ## Connects to MongoDB Atlas using your connection string from .env 
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL,tls=True, tlsCAFile=ca)

            ## Selects the database inside MongoDB. Like choosing which warehouse to go into.
            self.database=self.mongo_client[self.database]

            ## It should select the collection from self.database
            self.collection = self.database[self.collection]

            ## Inserts all records (list of JSON objects) into the collection at once.
            self.collection.insert_many(self.records)

            ## Returns the total number of records inserted.
            return(len(self.records))

        except Exception as e:
            raise NetworkSecurityException(e,sys)    


if __name__=='__main__':
    FILE_PATH="Network_Data\phisingData.csv"
    DATABASE="NetworkSecurityDB"
    Collection="NetworkData" 
    networkobj=NetworkDataExtract()
    records=networkobj.csv_to_json_conversion(file_path=FILE_PATH)
    print(records)
    no_of_records= networkobj.insert_data_to_mongoDb(records,DATABASE,Collection)
    print(no_of_records)   