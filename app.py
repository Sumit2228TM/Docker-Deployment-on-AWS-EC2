from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
from sklearn.linear_model import LinearRegression

app = FastAPI()

# Simple trained model
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([2, 4, 6, 8, 10])
model = LinearRegression()
model.fit(X, y)

class PredictionInput(BaseModel):
    value: float

@app.get("/")
def read_root():
    return {"message": "ML API v1.0", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/predict")
def predict(input: PredictionInput):
    prediction = model.predict([[input.value]])
    return {
        "input": input.value,
        "prediction": float(prediction[0])
    }

@app.get("/info")
def info():
    return {
        "model": "Linear Regression",
        "author": "Sumit Gatade",
        "version": "2.0"
    }