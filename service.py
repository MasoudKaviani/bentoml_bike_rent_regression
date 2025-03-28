import bentoml
import pandas as pd
from bentoml.io import JSON, PandasDataFrame
from pydantic import BaseModel

bento_model = bentoml.sklearn.get("bike_sharing_model:latest")
model_runner = bento_model.to_runner()

svc = bentoml.Service("bike_sharing_regressor", runners=[model_runner])

class BikeSharingInput(BaseModel):
    season: int
    yr: int
    mnth: int
    hr: int
    holiday: int
    weekday: int
    workingday: int
    weathersit: int
    temp: float
    atemp: float
    hum: float
    windspeed: float

@svc.api(
    input=JSON(pydantic_model=BikeSharingInput),
    output=JSON(),
)
async def predict_json(input_data: BikeSharingInput) -> dict:
    input_df = pd.DataFrame([input_data.dict()])
    prediction = await model_runner.predict.async_run(input_df)
    return {"predicted_demand": round(float(prediction[0]), 0)}

@svc.api(
    input=PandasDataFrame(),
    output=JSON(),
)
async def predict_dataframe(input_df: pd.DataFrame) -> dict:
    prediction = await model_runner.predict.async_run(input_df)
    return {"predictions": prediction.tolist()}