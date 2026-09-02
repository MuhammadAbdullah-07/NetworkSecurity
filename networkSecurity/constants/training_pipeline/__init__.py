import os
import sys
import pandas as pd
import numpy as np


## common/global constants that will be used across the whole project
ARGET_COLUMN = "Result"                    # the column you want to predict
PIPELINE_NAME: str = "NetworkSecurity"      # your pipeline name
ARTIFACT_DIR: str = "Artifacts"             # where all outputs are saved
FILE_NAME: str = "phishingData.csv"         # your main data file

TRAIN_FILE_NAME: str = "train.csv"          # training data file
TEST_FILE_NAME: str = "test.csv"            # testing data file


### DATA INGESTION CONSTANT USED ALL OVER THE PROJECT
 
DATA_INGESTION_COLLECTION_NAME: str = "NetworkData"         # COLLECTION name
DATA_INGESTION_DATABASE_NAME: str = "NetworkSecurityDB"     # DATABASE name
DATA_INGESTION_DIR_NAME: str = "data_ingestion"             # Dir name
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"     # Collection name
DATA_INGESTION_INGESTED_DIR: str = "ingested"               # ingested directory name
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2          # Train/test ratio