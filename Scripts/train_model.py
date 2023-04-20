"""
Script to load a dataset, train a series of ML models, and save them locally
"""
import os
import pickle
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from typing import Tuple


def load_dataset(data_path: str, col_names: list[str]) -> pd.DataFrame:
    """Function to load a dataset from memory

    :param data_path: File path to the data to be loaded
    :type data_path: str
    :param col_names: A list of the desired colun names
    :type col_names: list[str]
    :return: _description_
    :rtype: pd.DataFrame
    """
    # Load the iris dataset
    temp_df = pd.read_csv(data_path, header=None)
    # Give each column a meaninful name
    temp_df.columns = col_names
    # Create a label encoder
    label_encoder = LabelEncoder()
    # Assign labels to the iris species class
    temp_df["Label"] = label_encoder.fit_transform(temp_df["Class"])

    return temp_df


def split_dataset(df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Function to split a dataset 70/30 train/test

    :param df: Dataframe containing data to be split
    :type df: pd.DataFrame
    :return: _description_
    :rtype: Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]
    """    

    features = df.values[:, 0:4].reshape(len(df), 4)
    labels = df.values[:, 5]

    tr_X, ts_X, tr_y, ts_y = train_test_split(features, labels, test_size=0.3, random_state=42)
    tr_y = tr_y.astype('int')
    ts_y = ts_y.astype('int')

    return tr_X, ts_X, tr_y, ts_y


if __name__ == "__main__":
    print("Hello world")

    # Load the iris dataset
    iris_df = load_dataset(f"{os.getcwd()}/data/iris.data", ["Sepal Length", "Sepal Width",
                                              "Petal Length", "Petal Width", "Class"])

    # Split the data into train and test
    train_features, test_features, train_labels, test_labels = split_dataset(iris_df)

    # Train a range of basic ML models
    lr = LogisticRegression(random_state=0).fit(train_features, train_labels)
    knn = KNeighborsClassifier(n_neighbors=3).fit(train_features, train_labels)
    gnb = GaussianNB().fit(train_features, train_labels)
    dt = DecisionTreeClassifier().fit(train_features, train_labels)
    rf = RandomForestClassifier(max_depth=2, random_state=0).fit(train_features, train_labels)

    # Create list of models and model names
    models = [lr, knn, gnb, dt, rf]
    model_names = ["Logistic Regression", "K Nearest Neighbour", "Gaussian Naive Bayes",
                   "Decision Tree", "Random Forest"]

    # Iterate through the pairs of models and model names
    for model, name in zip(models, model_names):
        # Score the models on the test data and calculate accuracy
        print(f"{name} accuracy: {accuracy_score(model.predict(test_features), test_labels)}")
        # Save the model to the ../models directory
        pickle.dump(model, open(f"{os.getcwd()}/models/{name}.pkl", 'wb'))
