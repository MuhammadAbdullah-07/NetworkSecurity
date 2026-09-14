from networkSecurity.exception.exception import NetworkSecurityException
from networkSecurity.logging.logger import logger
from networkSecurity.constants.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME
import os
import sys


class NetworkModel:
# creating a class (NetworkModel) that combines TWO things together:
# 1. preprocessor (KNNImputer pipeline)
# 2. model (ML algorithm)
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor=preprocessor    # preprocessor → the KNNImputer pipeline (transforms data)
            self.model=model                  # model → the trained ML model (makes predictions)
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def predict(self,x):
        try:
            x_transform=self.preprocessor.transform(x)   # Takes new input data & transforms the input data using KNNImputer
            y_hat=self.model.predict(x_transform)        # model predicts phishing(1) or legitimate(0)
            return y_hat
        except Exception as e:
            raise NetworkSecurityException(e,sys)           