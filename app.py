## to trigger the training file
## it is the FRONT-END

import os
import sys
import json
import mlflow

## DagsHub credentials
os.environ["MLFLOW_TRACKING_URI"] = "https://dagshub.com/MuhammahAbdullah-07/NetworkSecurity.mlflow"
os.environ["MLFLOW_TRACKING_USERNAME"] = "MuhammahAbdullah-07"
os.environ["MLFLOW_TRACKING_PASSWORD"] = os.getenv("DAGSHUB_TOKEN")

import pymongo  ## to connect to MongoDB
from networkSecurity.exception.exception import NetworkSecurityException
from networkSecurity.logging.logger import logger
from networkSecurity.pipeline.training_pipeline import TrainingPipeline
from networkSecurity.utils.main_utils.utils import load_object
from networkSecurity.utils.ml_utils.model.estimator import NetworkModel
from networkSecurity.constants.training_pipeline import DATA_INGESTION_COLLECTION_NAME,DATA_INGESTION_DATABASE_NAME
from fastapi import FastAPI,File,UploadFile,Request
# FastAPI → creates the app
# File → to handle file inputs
# UploadFile → to accept uploaded files (CSV)
# Request → to handle incoming requests

from fastapi.middleware.cors import CORSMiddleware
# allows requests from different origins
# example: frontend on port 3000 calling API on port 8000

from uvicorn import run as app_run
# uvicorn is the server that runs FastAPI

from fastapi.responses import Response
# to send custom responses back to client

from starlette.responses import RedirectResponse
# to redirect user to another route
# example: redirect "/" to "/docs"

import pandas as pd

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")

from dotenv import load_dotenv
load_dotenv()


# then access your variables like:
MONGO_DB_URL = os.getenv("MONGODB_URI")
print(MONGO_DB_URL)

import certifi ## it is a python package that provide a set of root ceetificate, used to make a Secure HTTP connection 
ca=certifi.where()

client=pymongo.MongoClient(MONGO_DB_URL,tlsCAFile=ca)
database=client[DATA_INGESTION_DATABASE_NAME]
collection=database[DATA_INGESTION_COLLECTION_NAME]
# Create app object
app = FastAPI()
origins=["*"]   ## "*" means allow requests from ANY website


app.add_middleware(
    CORSMiddleware,  # adds CORS protection to your app `` CORS = Cross Origin Resource Sharing
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # allows all HTTP methods  / GET, POST, PUT, DELETE etc
    allow_headers=["*"]
)

# GET request
@app.get("/",tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipeline=TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("training is successful")
    except Exception as e:
        raise NetworkSecurityException(e,sys)

@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        
        ## Load preprocessor & model
        model = load_object("final_model/model.pkl")
        preprocessor = load_object("final_model/preprocessor.pkl")

        network_model=NetworkModel(preprocessor=preprocessor,model=model)

        print(df.iloc[0])
        y_pred=network_model.predict(df)
        print(y_pred)

        ## making predicted column
        df["Predicted_column"]=y_pred
        print(df["Predicted_column"])
        df["Predicted_column"] = df["Predicted_column"].replace({0: "Legitimate", 1: "Phishing"})

        df.to_csv("predicted_output/output.csv")
        ## Send to HTML
        return templates.TemplateResponse(
            request=request,
            name="table.html",
            context={
                "columns": df.columns.tolist(),
                "rows": df.values.tolist()
                }
                )
    except Exception as e:
        raise NetworkSecurityException(e, sys)    


if __name__=="__main__":
    app_run(app,host="0.0.0.0",port=8000)