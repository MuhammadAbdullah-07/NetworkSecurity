from networkSecurity.components.data_ingestion import DataIngestion
from networkSecurity.entity.config_entity import DataIngestionConfig
from networkSecurity.components.data_validation import DataValidation
from networkSecurity.entity.config_entity import DataValidationConfig
from networkSecurity.components.data_transformation import DataTransformation
from networkSecurity.entity.config_entity import DataTransformationConfig
from networkSecurity.entity.config_entity import ModelTrainerConfig
from networkSecurity.components.model_trainer import ModelTrainer
from networkSecurity.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact
from networkSecurity.logging.logger import logger
from networkSecurity.exception.exception import NetworkSecurityException
from networkSecurity.entity.config_entity import TrainingPipelineConfig
import sys

## To run this file

if __name__=="__main__":
    try:
        ## Requirements
        trainingpipelineconfig=TrainingPipelineConfig()
        ## Config settings
        dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)
        Data_ingestion=DataIngestion(dataingestionconfig)
        logger.info("Initiate the data ingestion from main.py")
        ##  The Function initiate_data_ingestion returns data_ingestion_artifact
        data_ingestion_artifact=Data_ingestion.initiate_data_ingestion()
        logger.info("Data initiation Started")
        print(data_ingestion_artifact)
        logger.info("Data initiation Completed")    

        ## Calling Data Validation
        ## Config settings

        data_validation_config=DataValidationConfig(trainingpipelineconfig)
        Data_Validation=DataValidation(data_ingestion_artifact,data_validation_config)
        logger.info("Initiate the data validation from main.py")
        data_validation_artifact=Data_Validation.initiate_data_validation()
        logger.info("Data Validation Started")
        print(data_validation_artifact)   
        logger.info("Data Validation Completed")

        
        ## Calling Data Transformation
        ## Config settings

        data_transformation_config=DataTransformationConfig(trainingpipelineconfig)
        Data_Transformation=DataTransformation(data_validation_artifact,data_transformation_config)
        logger.info("Initiate the data transformation  from main.py")
        data_transformation_artifact=Data_Transformation.initiate_data_transformation()
        logger.info("Data Transformation Started")
        print(data_transformation_artifact)
        logger.info("Data Transformation Completed")

        ## Calling MODEL TRAINER
        ## Config settings      
        model_trainer_config=ModelTrainerConfig(trainingpipelineconfig)
        model_trainer=ModelTrainer(data_transformation_artifact,model_trainer_config)  
        logger.info("Initiate the model trainer from main.py")
        model_trainer_artifact=model_trainer.initiate_model_trainer()
        logger.info("Model Trainer Started")
        print(model_trainer_artifact)
        logger.info("Model Trainer completed")
        
    except Exception as e:
        logger.error("Error occurred", exc_info=True)
        raise NetworkSecurityException(e,sys) 