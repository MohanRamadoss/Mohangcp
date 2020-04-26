from google.cloud import storage

from sklearn.linear_model import LinearRegression
from sklearn import preprocessing
from sklearn.pipeline import Pipeline
from sklearn.externals import joblib

import glob
import os
import subprocess
import sys
import pandas as pd

client = storage.Client(project='spikey-ml')
bucket = client.get_bucket('spikey_ml_engine')

# Loading Data
blob = bucket.blob("datasets/Automobile_data.csv")
blob.download_to_filename('Automobile_data.csv')
automobile = pd.read_csv('Automobile_data.csv')

# Cleaning Data
req_cols =['make','body-style','num-of-cylinders',\
           'engine-size','bore', 'horsepower','price']
           
automobile = automobile[req_cols]
automobile = automobile[automobile[automobile.columns] != '?']
automobile = automobile.dropna()

auto_features = automobile.drop('price', axis=1)
auto_target = automobile[['price']].apply(pd.to_numeric)

# label Encoding
le = preprocessing.LabelEncoder()
auto_features['num-of-cylinders'] = le.fit_transform(auto_features['num-of-cylinders'])

# One hot encoding
auto_features = pd.get_dummies(auto_features,
							   columns=['make','body-style']).apply(pd.to_numeric)

pipeline = Pipeline([
      ('linear', LinearRegression(fit_intercept=False))
    	])

pipeline.fit(auto_features, auto_target)

model = 'model.joblib'
joblib.dump(pipeline, model)

# Upload the saved model file to Cloud Storage
print('Uploading Model to Google Cloud Storage')
model_path = os.path.joinmodel_path = os.path.join('gs://spikey_ml_engine/sklearn_model/', model)
subprocess.check_call(['gsutil', 'cp', model, model_path], stderr=sys.stdout)

























