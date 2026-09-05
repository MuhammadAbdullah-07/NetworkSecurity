## Artifact Entity (artifact_entity.py) : Defines what results each component gives as OUTPUT:
##      Data Ingestion
##    → produces DataIngestionArtifact (trained_file_path, test_file_path)
##          ↓
##      Data Validation
##    → receives DataIngestionArtifact as INPUT
##    → produces DataValidationArtifact as OUTPUT
##          ↓
##      Data Validation

from dataclasses import dataclass

@dataclass                      ## uses as Decorator
class DataIngestionArtifact:    ## make 2 paramters
    trained_file_path:str       ## 1st paramter
    test_file_path:str          ## 2nd paramter  

@dataclass
class DataValidationArtifact:
    validation_status : bool
    valid_train_file_path: str
    valid_test_file_path : str
    invalid_train_file_path: str
    invalid_test_file_path : str
    drift_report_file_path: str
       