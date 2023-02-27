# AF-Model-Scoring
Azure Functions are a fantastic way to deploy real time endpoints for model scoring, this repo will contain a complete guide and worked examples on how to quickly and easily deploy your mode for real time scoring using Azure Functions. 

# Setup
Below are a set of instruction on how to set up the various tools and services required.

## Python virtual environment
All of the following commands should be run in a terminal on a machine with python installed a python download can be found [here](https://www.python.org/downloads/).
1) Create the virtual environment:
```
$py -m venv venv
```
2) Activate the virtual enviornment:
```
.\.venv\Scripts\activate
```
3) Done. It is as easy as that!
Bonus step is to install of all the required python packages from the requirements.txt
- Install the requirements:
```
pip install -r requirements.txt
```

## MLFlow Connection
As part of the advanced function models will be registered to, and loaded directly from MLFlow in DataBricks, the below instructions will outline how to connect from your local machine to MLFlow.
1) Generate a token from DataBricks by going to *User Settings* -> *Access tokens* -> *Generate new token*
2) Run the following command:
```
databricks configure --token
```
3) Enter the databricks host URL & Token into the prompts
4) Create an environment variable for the expierment being used for this demo:
- Windows:
```
set IRIS_EXPERIMENT=<Experiment URL>
```
- Linux:
```
export IRIS_EXPERIMENT=<Experiment URL>
```