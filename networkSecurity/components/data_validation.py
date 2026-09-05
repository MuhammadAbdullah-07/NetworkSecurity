from networkSecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networkSecurity.entity.config_entity import DataValidationConfig
from networkSecurity.exception.exception import NetworkSecurityException
from networkSecurity.logging.logger import logger
from networkSecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from scipy.stats import ks_2samp
import pandas as pd
import os,sys
## importing the function
from networkSecurity.utils.main_utils.utils import read_yaml_file,write_yaml_file

class DataValidation:

    ## Taking data_ingestion_artifact as Input
    ## Taking data_validation_config as output     
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config

            ## Create a function with read_yaml_file name in Utils. Which opens and read the yaml file
            ## Yaml file contain a fixed format for our data
            self._schema_config=read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    ## function for reading the data 
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
         try:
              return pd.read_csv(file_path)
         except Exception as e:
              raise NetworkSecurityException(e,sys) 

    ## function for validating the columns  
    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
         try:
              numbers_of_columns=len(self._schema_config["columns"])
              logger.info(f"required number of columns:{numbers_of_columns}")
              logger.info(f"dataframe has columns:{dataframe.columns}")
              if (numbers_of_columns)== len(dataframe.columns):
                   return True
              return False
         except Exception as e:
            raise NetworkSecurityException(e,sys) 

    def detect_dataset_drift(self,base_df,current_df,threshold=0.05)->bool:
         try:
              status=True
              report={}
              for column in base_df.columns:
                   d1=base_df[column] ## original df
                   d2=current_df[column] ## Current df
                   ## Comparing both df
                   is_same_dist=ks_2samp(d1,d2)

                   if threshold <= is_same_dist.pvalue:
                        is_found=False
                   else:
                        is_found=True
                        status=False     
                   ## Storing / Updating the report
                   report.update({column:{
                         "p_value":float(is_same_dist.pvalue),
                         "drift_status":is_found
                    }})   

              drift_report_file_path=self.data_validation_config.drift_report_file_path  
              ## Making directory for storing this file
              dir_path=os.path.dirname(drift_report_file_path)
              os.makedirs(dir_path,exist_ok=True) 

              write_yaml_file(file_path=drift_report_file_path,content=report)
              return status
                    
         except Exception as e:
              raise NetworkSecurityException(e,sys)          

    def initiate_data_validation(self)->DataValidationArtifact: ## DataValidationArtifact is return type
            try:
                ## to validate data, first we need data FROM DATA-INGESTION
                train_file_path=self.data_ingestion_artifact.trained_file_path
                test_file_path=self.data_ingestion_artifact.test_file_path 

                ## Reaading the data as train & test 

                train_dataframe=DataValidation.read_data(train_file_path)
                test_dataframe=DataValidation.read_data(test_file_path)

                ## Validate the number_of_columns for training data
                status=self.validate_number_of_columns(dataframe=train_dataframe)
                if not status:
                     error_message=f"train dataframe doesnot contain all the columns" 

                ## Validate the number_of_columns for Test data
                status=self.validate_number_of_columns(dataframe=test_dataframe)
                if not status:
                     error_message=f"Test dataframe doesnot contain all the columns"  

                ## Checking Data Drift
                status=self.detect_dataset_drift(base_df=train_dataframe,current_df=test_dataframe)
                dir_path=os.path.dirname(self.data_validation_config.valid_train_file_path)
                os.makedirs(dir_path,exist_ok=True)

                ## Converting Train-dataframe to csv 
                train_dataframe.to_csv(
                     self.data_validation_config.valid_train_file_path,index=False,header=True
                )
                ## Converting Test-dataframe to csv 
                test_dataframe.to_csv(
                     self.data_validation_config.valid_test_file_path,index=False,header=True
                )

                ##  return type

                self.data_validation_artifact=DataValidationArtifact(
                     validation_status= status,
                     valid_train_file_path= self.data_ingestion_artifact.trained_file_path,
                     valid_test_file_path= self.data_ingestion_artifact.test_file_path,
                     invalid_train_file_path= None,
                     invalid_test_file_path= None,
                     drift_report_file_path=self.data_validation_config.drift_report_file_path
                )

                return self.data_validation_artifact
                                         
            except Exception as e:
                 raise NetworkSecurityException(e,sys)