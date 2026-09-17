from networkSecurity.components.data_ingestion import DataIngestion
from networkSecurity.entity.config_entity import DataIngestionConfig
from networkSecurity.components.data_validation import DataValidation
from networkSecurity.entity.config_entity import DataValidationConfig
from networkSecurity.components.data_transformation import DataTransformation
from networkSecurity.entity.config_entity import DataTransformationConfig
from networkSecurity.entity.config_entity import ModelTrainerConfig
from networkSecurity.components.model_trainer import ModelTrainer
from networkSecurity.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact,ModelTrainerArtifact
from networkSecurity.logging.logger import logger
from networkSecurity.exception.exception import NetworkSecurityException
from networkSecurity.entity.config_entity import TrainingPipelineConfig
import sys
from networkSecurity.constants.training_pipeline import TRAINING_BUCKET_NAME
from networkSecurity.cloud.s3_syncer import S3Sync

class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config=TrainingPipelineConfig()
        self.s3_sync=S3Sync()

    def start_data_ingestion(self):
        try:
            self.data_ingesion_config=DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            logger.info("Data Ingestion initaited")
            Data_ingestion=DataIngestion(data_ingestion_config=self.data_ingesion_config)
            data_ingeston_artifact=Data_ingestion.initiate_data_ingestion()
            logger.info("Data initiation Completed")

            return data_ingeston_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)   

    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact):
        try:
            self.data_validation_config=DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            logger.info("Data Validation initaited")
            Data_validation=DataValidation(data_validation_config=self.data_validation_config,
                                           data_ingestion_artifact=data_ingestion_artifact)
            data_validation_artifact=Data_validation.initiate_data_validation()
            logger.info("Data Validation Completed")

            return data_validation_artifact
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)  

    def start_data_transformation(self,data_validation_artifact:DataValidationArtifact):
        try:
            self.data_transformation_config=DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            logger.info("Data Transformation initaited")
            Data_transformation=DataTransformation(data_transformation_config=self.data_transformation_config,
                                           data_validation_artifact=data_validation_artifact)
            data_transformation_artifact=Data_transformation.initiate_data_transformation()
            logger.info("Data Transformatiom Completed")

            return data_transformation_artifact
            
        except Exception as e:
            raise NetworkSecurityException(e,sys) 

    def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifact)->ModelTrainerArtifact:
        try:
            self.model_trainer_config=ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            logger.info("Model Trainer initaited")
            Model_trainer=ModelTrainer(model_trainer_config=self.model_trainer_config,
                                           data_transformation_artifact=data_transformation_artifact)
            model_trainer_artifact=Model_trainer.initiate_model_trainer()
            logger.info("Model Trainer Completed")

            return model_trainer_artifact
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)   

    def sync_artifact_dir_to_s3(self):
        try:
            aws_bucket_url=f"s3://{TRAINING_BUCKET_NAME}/artifact/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder=self.training_pipeline_config.artifacts_dir,aws_bucket_url=aws_bucket_url)    
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def sync_final_model_to_s3(self):
        try:
            aws_bucket_url=f"s3://{TRAINING_BUCKET_NAME}/final_model/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder=self.training_pipeline_config.model_dir,aws_bucket_url=aws_bucket_url)    
        except Exception as e:
            raise NetworkSecurityException(e,sys)        


    def run_pipeline(self):   ## this function will be used in our app.py
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)

            ## Pushing into s3 bucket
            self.sync_artifact_dir_to_s3()
            self.sync_final_model_to_s3() 


            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)                                        