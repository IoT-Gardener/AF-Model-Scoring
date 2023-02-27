import json
import logging
import mlflow
import os
import pickle
import azure.functions as func
import numpy as np
from pydantic import BaseModel, ValidationError
from mlflow.tracking import MlflowClient

# Setup the MLFlow client
mlflow_uri = "databricks"
client = MlflowClient(tracking_uri=mlflow_uri)
mlflow.set_tracking_uri(mlflow_uri)

# Create variable to store the model
MODEL = None

class IrisInput(BaseModel):
    """
    Class to define the structure for the Unemployment model input data
    """
    Sepal_Length: float
    Sepal_Width: float
    Petal_Length: float
    Petal_Width: float


def load_model():
    """
    Function to load the model from MLFlow and assign it to the global MODEL variable
    """
    global MODEL
    MODEL = mlflow.sklearn.load_model(model_uri="models:/sk-learn-Random Forest-reg-model/Production")
    logging.info("Successfully loaded model sk-learn-Random Forest-reg-model from MLFlow")


def return_error(msg: str) -> func.HttpResponse:
    """Function to create http response for any given error

    :param msg: The message to add to the response
    :type msg: str
    :return: Returns a HttpResponse for the relevant issue
    :rtype: func.HttpResponse
    """
    return func.HttpResponse(body=msg, 
                             headers={"Content-Type": "application/json"},
                             status_code=500
    )


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Check if reload was called
    reload_flag = req.route_params.get('reload')
    if reload_flag == "reload":
        try:
            logging.info("Reloading model")
            load_model()
        except Exception as e:
            logging.error(f"Error loading model, {e}")
            return return_error("Error loading model")
        # If the model is successful reloaded return a 200 response
        return func.HttpResponse(body="Model successfully reloaded",
                                 headers={"Content-Type": "application/json"},
                                 status_code=200
        )

    # Read the message body
    try:
        json_msg = req.get_json()
        logging.info(f"Json message recieved: {json_msg}")
    except ValueError:
        logging.error("No json message recieved.")
        return return_error("No json message recieved")

    # Validate the input
    try:
        IrisInput(**json_msg)
        logging.info("Input validated successfully")
    except ValidationError as e:
        logging.error(f"Message validation failed, {e}")
        return return_error(f"Request validation error, {e}")

    # If there is no model loaded, load the model
    if MODEL == None:
        try:
            logging.info("Loading model")
            load_model()
        except Exception as e:
            logging.error(f"Failed to load model, {e}")
            return return_error("Failed to load model")

    # Preprocess data for the model
    try:
        # Convert the input dict to a numpy array compatible with the model
        model_inpt = np.array(list(json_msg.values())).reshape(1,-1)
        logging.info(f"Model input: {model_inpt}")
    except Exception as e:
        logging.error(f"Failed preparing data for model, {e}")
        return return_error("Failed preparing data for model")

    # Query the model
    try:
        prediction = MODEL.predict(model_inpt)
        logging.info(f"Prediction: {prediction}")
    except Exception as e:
        logging.error(f"Failed to query model, {e}")
        return return_error("Failed to query model")

    # Format output 
    output = {
                "Prediction": int(prediction[0]),
                "Model": "Random Forest",
                "Input": json_msg
             }

    return func.HttpResponse(body=json.dumps(output),
                             headers={"Content-Type": "application/json"},
                             status_code=200
    )
