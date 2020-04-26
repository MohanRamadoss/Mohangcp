from sklearn.linear_model import LinearRegression
from sklearn import preprocessing
from sklearn.pipeline import Pipeline
import pickle
import pandas as pd

automobile = pd.read_csv('../input/Automobile_data.csv')

# Cleaning Data
req_cols =['make','wheel-base','body-style','num-of-cylinders',\
           'engine-size','bore', 'horsepower','peak-rpm','price']
           
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

with open('model.pkl', 'wb') as model_file:
    pickle.dump(pipeline, model_file)