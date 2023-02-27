import mlflow
import mlflow.sklearn
import os
import pickle
from mlflow.tracking import MlflowClient


mlflow_uri = "databricks"
client = MlflowClient(tracking_uri=mlflow_uri)
mlflow.set_tracking_uri(mlflow_uri)

if __name__ == "__main__":
    # Create list of models
    models = os.listdir(f"{os.getcwd()}/models")

    # Set the MLFlow experiment from the URL
    experiment_name = os.getenv("IRIS_EXPERIMENT")
    print(experiment_name)
    mlflow.set_experiment(experiment_name=experiment_name)

    # Start an MLFlow run
    with mlflow.start_run(run_name="Python SKLearn Models") as run:
        # Iterate over each model created
        for model_name in models:
            # Load the model
            model = pickle.load(open(f"{os.getcwd()}/models/{model_name}", 'rb'))
            # Log the sklearn model and register 
            mlflow.sklearn.log_model(
                sk_model=model,
                artifact_path=f'{model_name.split(".")[0]}-model',
                registered_model_name=f'sk-learn-{model_name.split(".")[0]}-reg-model'
            )
