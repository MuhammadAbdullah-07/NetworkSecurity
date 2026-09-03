from dataclasses import dataclass

@dataclass                      ## uses as Decorator
class DataIngestionArtifact:    ## make 2 paramters
    trained_file_path:str       ## 1st paramter
    test_file_path:str          ## 2nd paramter  