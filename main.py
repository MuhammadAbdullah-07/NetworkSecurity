from networkSecurity.components.data_ingestion import DataIngestion
from networkSecurity.logging.logger import logger
from networkSecurity.exception.exception import NetworkSecurityException
from networkSecurity.entity.config_entity import DataIngestionConfig
from networkSecurity.entity.config_entity import TrainingPipelineConfig
import sys

## To run this file

if __name__=="__main__":
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)
        Data_ingestion=DataIngestion(dataingestionconfig)
        logger.info("Initiate the data ingestion from main.py")
        ##  The Function initiate_data_ingestion returns data_ingestion_artifact
        data_ingestion_artifact=Data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifact)

    except Exception as e:
        logger.error("Error occurred", exc_info=True)
        raise NetworkSecurityException(e,sys) 