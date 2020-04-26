import sys
import glob
import os
import subprocess
import pickle

import pandas as pd
import xgboost as xgb
from sklearn import preprocessing
from google.cloud import storage

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

dtrain = xgb.DMatrix(auto_features, label=auto_target)
bst = xgb.train({}, dtrain, 20)

model = 'model.bst'
bst.save_model(model)

# Upload the saved model file to Cloud Storage
model_path = os.path.join('gs://spikey_ml_engine/xgb_model/', model)
subprocess.check_call(['gsutil', 'cp', model, model_path], stderr=sys.stdout)






















