import pickle
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import bentoml

data = pd.read_csv('data/hour.csv')
data = data.drop(['instant', 'dteday', 'casual', 'registered'], axis=1)

X = data.drop('cnt', axis=1)
y = data['cnt']

categorical_features = ['season', 'yr', 'mnth', 'hr', 'holiday', 'weekday', 'workingday', 'weathersit']
numerical_features = ['temp', 'atemp', 'hum', 'windspeed']

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])

model = Pipeline([
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

model.fit(X, y)

bento_model = bentoml.sklearn.save_model(
    "bike_sharing_model",
    model,
    signatures={
        "predict": {
            "batchable": True,
            "batch_dim": 0,
        }
    },
    metadata={
        "dataset": "bike_sharing",
        "model_type": "RandomForestRegressor"
    }
)

print(f"Model saved: {bento_model}")