import os
import numpy as np

## common/global constants that will be used across the whole project
TARGET_COLUMN = "Result"                    # the column you want to predict
PIPELINE_NAME: str = "NetworkSecurity"      # your pipeline name
ARTIFACT_DIR: str = "Artifacts"             # where all outputs are saved
FILE_NAME: str = "phishingData.csv"         # your main data file

TRAIN_FILE_NAME: str = "train.csv"          # training data file
TEST_FILE_NAME: str = "test.csv"            # testing data file

SCHEMA_FILE_PATH=os.path.join("data_schema","schema.yaml")


### DATA INGESTION CONSTANT USED ALL OVER THE PROJECT
 
DATA_INGESTION_COLLECTION_NAME: str = "NetworkData"         # COLLECTION name
DATA_INGESTION_DATABASE_NAME: str = "NetworkSecurityDB"     # DATABASE name
DATA_INGESTION_DIR_NAME: str = "data_ingestion"             # Dir name
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"     # Collection name -- for Whole data
DATA_INGESTION_INGESTED_DIR: str = "ingested"               # ingested directory name -- for Train / Test
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2          # Train/test ratio


### DATA VALIDATION CONSTANT USED ALL OVER THE PROJECT

DATA_VALIDATION_DIR_NAME:str= "data_validation"
DATA_VALIDATION_VALID_DIR :str= "validated"
DATA_VALIDATION_INVALID_DIR :str= "invalidated"
DATA_VALIDATION_DRIFT_REPORT_DIR :str= "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME :str= "report.yaml"


### DATA TRANSFORMATION CONSTANT USED ALL OVER THE PROJECT

DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"              # folder where all transformation files go
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"          # Folder having transformed train.npy & test.npy are saved
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object" # Folder where preprocessing.pkl is saved
PREPROCESSING_OBJECT_FILE_NAME="preprocessing.pkl"                     # Name of the saved preprocessor file (KNNImputer saved here)

## KNN imputer to replace Nan values
DATA_TRANSFORMATION_IMPUTER_PARAMS: dict={
    "missing_values" : np.nan,
    "n_neighbors" : 3,
    "weights" : "uniform",
}
