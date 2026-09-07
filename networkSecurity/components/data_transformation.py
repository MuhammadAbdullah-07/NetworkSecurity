import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networkSecurity.exception.exception import NetworkSecurityException
from networkSecurity.logging.logger import logger

## for data transformation we need to drop target columns
from networkSecurity.constants.training_pipeline import TARGET_COLUMN

# As we gonna do FE, we have to import imputer params
from networkSecurity.constants.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from networkSecurity.entity.artifact_entity import DataTransformationArtifact ## it is depend on validation so
from networkSecurity.entity.artifact_entity import DataValidationArtifact
from networkSecurity.entity.config_entity import DataTransformationConfig

## Importing functions 
from networkSecurity.utils.main_utils.utils import save_numpy_array_data,save_object


class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,
                 data_transformation_config: DataTransformationConfig):
        try:
            self.data_validation_artifact=data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys) 
    
    @staticmethod
    ## initiate the imputer
    def get_data_transformer_object()-> Pipeline:
        try:
            imputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            preprocessor=Pipeline(steps=[("imputer",imputer)])
            return preprocessor
        except Exception as e:
            raise NetworkSecurityException(e,sys)        

    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            logger.info("We are iniiating the Data Transformation")
            train_df=DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            ## REMOVING TARGET COLUMN FROM TRAINING DATAFRAME
            input_features_train_df=train_df.drop(columns=[TARGET_COLUMN]) ## X
            target_feature_train_df=train_df[TARGET_COLUMN] ## y 
            ## Replacing the values of Target feature values with 0,1
            target_feature_train_df=target_feature_train_df.replace(-1,0) ## replacing -1 with 0

            ## REMOVING TARGET COLUMN FROM TEST DATAFRAME
            input_features_test_df=test_df.drop(columns=[TARGET_COLUMN]) ## X
            target_feature_test_df=test_df[TARGET_COLUMN] ## y  
            ## Replacing the values of Target feature values with 0,1
            target_feature_test_df=target_feature_test_df.replace(-1,0) ## replacing -1 with 0

            ## Calling the function inside the class
            preprocessor=self.get_data_transformer_object()

            ## Using this for transforming on my training df
            transformed_input_features_train_df=preprocessor.fit_transform(input_features_train_df)
            transformed_input_features_test_df=preprocessor.transform(input_features_test_df)

            # Combining transformed train features + train target
            train_arr=np.c_[transformed_input_features_train_df,np.array(target_feature_train_df)]
            test_arr=np.c_[transformed_input_features_test_df,np.array(target_feature_test_df)]

            ## Saving the arr to Save function we created in utils
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,array=test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path,obj=preprocessor)


            ## Return of initiate function
            data_transformation_artifact=DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )

            return data data_transformation_artifact
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)   