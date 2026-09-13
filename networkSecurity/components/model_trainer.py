import pandas as pd
import numpy as np
import os
import sys
from networkSecurity.exception.exception import NetworkSecurityException
from networkSecurity.logging.logger import logger
from networkSecurity.entity.config_entity import ModelTrainerConfig
from networkSecurity.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact
from networkSecurity.utils.main_utils.utils import save_object,load_object,load_numpy_array_data,evaluate_models
from networkSecurity.utils.ml_utils.metrics.classification_metric import get_classificiation_score
from networkSecurity.utils.ml_utils.model.estimator import NetworkModel
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier,AdaBoostClassifier
import mlflow

class ModelTrainer:
    def __init__(self,data_transformation_artifact:DataTransformationArtifact,
                 model_trainer_config:ModelTrainerConfig):
        try:
            self.data_transformation_artifact=data_transformation_artifact
            self.model_trainer_config=model_trainer_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def track_mlflow(self,best_model,classificationmetric):
        with mlflow.start_run():
            f1_score=classificationmetric.f1_score
            precision_score=classificationmetric.precision_score
            recall_score=classificationmetric.recall_score
            


            mlflow.log_metric("f1_score",f1_score)
            mlflow.log_metric("precision_score",precision_score)
            mlflow.log_metric("recall_score",recall_score)

            mlflow.sklearn.log_model(best_model,"model")
            


    def train_model(self,X_train,y_train,X_test,y_test):
        models={
            "LogisticRegression": LogisticRegression(verbose=1),
            "KNeighborsClassifier" : KNeighborsClassifier(),
            "DecisionTreeClassifier" : DecisionTreeClassifier(),
            "RandomForestClassifier":RandomForestClassifier(verbose=1),
            "GradientBoostingClassifier":GradientBoostingClassifier(verbose=1),
            "AdaBoostClassifier":AdaBoostClassifier()
        } 
        params = {
                "LogisticRegression": {
                    "C": [0.1, 1, 10],                        # regularization strength
                    "solver": ["lbfgs", "liblinear"],          # optimization algorithm
                    "max_iter": [100, 200, 500]                # maximum iterations
                    },
                "KNeighborsClassifier": {
                    "n_neighbors": [3, 5, 7, 9],              # number of neighbors
                    "weights": ["uniform", "distance"],        # weight function
                    "metric": ["euclidean", "manhattan"]       # distance metric
                    },
              "DecisionTreeClassifier": {
                    "criterion": ["gini", "entropy"],          # splitting criteria
                    "max_depth": [3, 5, 7, None],             # max depth of tree
                    "min_samples_split": [2, 5, 10],          # min samples to split
                    "min_samples_leaf": [1, 2, 4]             # min samples in leaf
                    },
                "RandomForestClassifier": {
                    "n_estimators": [100, 200, 300],          # number of trees
                    "criterion": ["gini", "entropy"],          # splitting criteria
                    "max_depth": [3, 5, 7, None],             # max depth of tree
                    "min_samples_split": [2, 5, 10],          # min samples to split
                    },
                "GradientBoostingClassifier": {
                    "n_estimators": [100, 200, 300],          # number of trees
                    "learning_rate": [0.01, 0.05, 0.1],       # learning rate
                    "max_depth": [3, 5, 7],                   # max depth of tree
                    "subsample": [0.8, 0.9, 1.0]             # fraction of samples
                    },
                "AdaBoostClassifier": {
                    "n_estimators": [50, 100, 200],           # number of estimators
                    "learning_rate": [0.01, 0.05, 0.1, 1.0]  # learning rate
                    }}
        
        ## give report of each model with name and score
        model_report:dict=evaluate_models(X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test,models=models,params=params)

        ## Getting best model with best score
        best_model_score=max(sorted(model_report.values()))

        ## Getting best model name
        best_model_name=list(model_report.keys())[
            list(model_report.values()).index(best_model_score)
            ]

        best_model=models[best_model_name]

        ## training this best model on X_train
        y_train_pred=best_model.predict(X_train)
        classificaton_train_metric=get_classificiation_score(y_true=y_train,y_pred=y_train_pred)

        ## here we track the experiment with ML flow
        self.track_mlflow(best_model,classificaton_train_metric)

        ## training this best model on X_test
        y_test_pred=best_model.predict(X_test)
        classificaton_test_metric=get_classificiation_score(y_true=y_test,y_pred=y_test_pred)
        ## here we track the experiment with ML flow
        self.track_mlflow(best_model,classificaton_test_metric)

        ## loading the preprocessor (knn imputer)
        preprocessor=load_object(file_path=self.data_transformation_artifact.transformed_object_file_path
        )

        model_dir_path=os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path,exist_ok=True)

        network_model=NetworkModel(preprocessor=preprocessor,model=best_model)
        save_object(self.model_trainer_config.trained_model_file_path,obj=network_model)

        model_trainer_artifact=ModelTrainerArtifact(
            trained_model_file_path=self.model_trainer_config.trained_model_file_path,
            train_metric_artifact=classificaton_train_metric,
            test_metric_artifact=classificaton_test_metric
            )

        logger.info(f"Model Trainer Artifact:{model_trainer_artifact}")    

        return model_trainer_artifact
        



    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            train_file_path=self.data_transformation_artifact.transformed_train_file_path
            test_file_path=self.data_transformation_artifact.transformed_test_file_path

            ## loading the numpy array
            train_arr=load_numpy_array_data(train_file_path)
            test_arr=load_numpy_array_data(test_file_path)

            # Check for NaN
            print("Train NaN count:", np.isnan(train_arr).sum())
            print("Test NaN count:", np.isnan(test_arr).sum())

            ## spliting X_train,y_train,X_test,y_test
            X_train,y_train,X_test,y_test=(
                train_arr[:,:-1], ## X_train
                train_arr[:,-1],  ## y_train
                test_arr[:,:-1],  ## X_test
                test_arr[:,-1]    ## y_test
            )
            

            ## make a model function that will work on X_train and y_train
            model_trainer_artifact=self.train_model(X_train,y_train,X_test,y_test)
            return model_trainer_artifact



        except Exception as e:
            raise NetworkSecurityException(e,sys)        
        