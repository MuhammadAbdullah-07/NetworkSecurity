from networkSecurity.components.data_ingestion import DataIngestion
from networkSecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig
from networkSecurity.components.data_validation import DataValidation
from networkSecurity.entity.config_entity import DataValidationConfig
from networkSecurity.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
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
        
        logger.info("Data initiation Completed")
        print(data_ingestion_artifact)

        ## Calling Data Validation

        ## Config settings

        data_validation_config=DataValidationConfig(trainingpipelineconfig)
        Data_Validation=DataValidation(data_ingestion_artifact,data_validation_config)
        logger.info("Initiate the data validation from main.py")
        data_validation_artifact=Data_Validation.initiate_data_validation()
        logger.info("Data Validation Completed")
        print(data_validation_artifact)        

    except Exception as e:
        logger.error("Error occurred", exc_info=True)
        raise NetworkSecurityException(e,sys) 