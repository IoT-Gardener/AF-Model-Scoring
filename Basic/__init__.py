import json
import logging
import os
import pickle
import azure.functions as func
import numpy as np

def return_error(msg: str) -> func.HttpResponse:
    """Function to create http response for any given error

    :param msg: The message to add to the response
    :type msg: str
    :return: Returns a HttpResponse for the relevant issue
    :rtype: func.HttpResponse
    """
    return func.HttpResponse(body=f"{msg}", 
                             headers={"Content-Type": "application/json"},
                             status_code=500)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Read the message body
    try:
        json_msg = req.get_json()
        logging.info(f"Json message recieved: {json_msg}")
    except ValueError:
        logging.error("No json message recieved.")
        return return_error("No json message recieved")

    # Load the model
    try:
        model = pickle.load(open(f"{os.getcwd()}/models/Random Forest.pkl", 'rb'))
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
        prediction = model.predict(model_inpt)
        logging.info(f"Prediction: {prediction}")
    except Exception as e:
        logging.error(f"Failed to query model, {e}")
        return return_error("Failed to query model")

    return func.HttpResponse(f"{prediction}",
                             headers={"Content-Type": "application/json"},
                             status_code=200)
