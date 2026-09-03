from networkSecurity.exception.exception import NetworkSecurityException
from networkSecurity.logging.logger import logger

## Configuration of Data Ingestion Config

from networkSecurity.entity.config_entity import DataIngestionConfig
from networkSecurity.entity.artifact_entity import DataIngestionArtifact
import os
import sys
import pymongo
import numpy as np
import pandas as pd
from typing import List
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
load_dotenv()

MONGODB_URI=os.getenv("MONGODB_URI")

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def export_collection_as_dataframe(self):
        """
        READ THE DATA FROM MONGODB and convert it into DF
        """
        try:
            ## Assigning variable to the database_name and database_collection 
            database_name=self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collection_name

            ## Calling the mongoclient-- getting Data fron MongoDB
            self.mongo_client=pymongo.MongoClient(MONGODB_URI)

            ## Setting variable
            collection=self.mongo_client[database_name][collection_name]

            ## Changing it into DF
            df=pd.DataFrame(list(collection.find()))

            ## Dropping the id columns
            if "_id" in df.columns.to_list():
                df=df.drop(columns=["_id"])

            df.replace({"na" :np.nan},inplace=True)
            return df    

        except Exception as e:
            raise NetworkSecurityException(e,sys)    

        """
        Export data to feature store-- store all data
        """
    def export_data_to_feature_store(self,dataframe: pd.DataFrame):
        try:
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path

            ## Creating Folder
            dir_path=os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)

            ## converting dataframe into csv
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e,sys)    

    def  split_data_as_train_test(self,dataframe: pd.DataFrame):
        try:
            train_set,test_set=train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio)
            logger.info("Performing Train Test split on Dataframe")

            ## Making dir for storing training data and testing data
            dir_path=os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True) 

            logger.info("Exporting Train & Test file path")

            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index=False,header=True
            )

            test_set.to_csv(
                self.data_ingestion_config.testing_file_path, index=False,header=True
            )            

            logger.info("Train & Test file path Exported !")
        except Exception as e:
            raise NetworkSecurityException(e,sys)   



    def initiate_data_ingestion(self):
        try:
            dataframe= self.export_collection_as_dataframe() 
            dataframe=self.export_data_to_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)

            ## Caliing from entity.artifact_entity.py
            data_ingestion_artifact=DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,test_file_path=self.data_ingestion_config.testing_file_path )

            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)    
        