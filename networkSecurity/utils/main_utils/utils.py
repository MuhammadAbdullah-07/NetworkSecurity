import yaml
import os
import sys
import numpy as np
import pickle
from networkSecurity.exception.exception import NetworkSecurityException
from networkSecurity.logging.logger import logger
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score


def read_yaml_file(file_path : str) -> dict:
    try:
        with open(file_path,"rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)

def write_yaml_file(file_path : str, content : object,replace : bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"w") as file:
            yaml.dump(content,file)        
        
    except Exception as e:
        raise NetworkSecurityException(e,sys)    


### SAVING THE NUMPY DATA ARRAY        
def save_numpy_array_data(file_path : str, array : np.array):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            np.save(file_obj,array,allow_pickle=True)
    except Exception as e:
        raise NetworkSecurityException(e,sys)

### KNN imouter creates a Pickle file which is need to be saved!
def save_object(file_path : str , obj : object):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            pickle.dump(obj,file_obj)

            logger.info("Pickle filed is dumped ! ")
    except Exception as e:
        raise NetworkSecurityException(e,sys)        

## General func for loading the pickle file

def load_object(file_path : str) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"file path {file_path} is not available")
        with open (file_path,"rb") as file_obj:
            print(file_obj)
            return pickle.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys)    

## General func for loading the Numpy array

def load_numpy_array_data(file_path : str) -> np.array:
    try:
        with open (file_path,"rb") as file_obj:
            print(file_obj)
            return np.load(file_obj,allow_pickle=True)
    except Exception as e:
        raise NetworkSecurityException(e,sys)    

def evaluate_models(X_train,y_train,X_test,y_test,models,params):
    try:
        report = {}
        for i in range(len(list(models))):
            model=list(models.values())[i]
            param=params[list(models.keys())[i]]
            grid=GridSearchCV(
                estimator=model,
                param_grid=param,
                cv=3,
                n_jobs=1)
            grid.fit(X_train,y_train)
            model.set_params(**grid.best_params_)
            model.fit(X_train,y_train)

            ## prediction for train & test data

            y_train_pred=model.predict(X_train)
            y_test_pred=model.predict(X_test)

            ## accuracy score for train & test data
            train_accuracy_score=accuracy_score(y_train,y_train_pred)
            test_accuracy_score=accuracy_score(y_test,y_test_pred)

            ## storing result back to report 
            report[list(models.keys())[i]] = test_accuracy_score

        return report

    except Exception as e:
        raise NetworkSecurityException(e,sys)        