from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd

app = FastAPI(title="AutoOracle AI API", version="1.0.0")

# Allow requests from the Vite dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model once at startup
model = joblib.load("car_prediction_model_sl.pkl")

class CarInput(BaseModel):
    year: int
    present_price: float
    kms_driven: int
    fuel_type: str        # "Petrol" | "Diesel" | "CNG"
    seller_type: str      # "Dealer" | "Individual"
    transmission: str     # "Manual" | "Automatic"
    owner: int

@app.get("/")
def root():
    return {"status": "AutoOracle AI API is running"}

@app.post("/predict")
def predict(car: CarInput):
    fuel_map        = {"Petrol": 0, "Diesel": 1, "CNG": 2}
    seller_map      = {"Dealer": 0, "Individual": 1}
    transmission_map = {"Manual": 0, "Automatic": 1}

    input_df = pd.DataFrame([{
        "Year":         car.year,
        "Present_Price": car.present_price,
        "Kms_Driven":   car.kms_driven,
        "Fuel_Type":    fuel_map[car.fuel_type],
        "Seller_Type":  seller_map[car.seller_type],
        "Transmission": transmission_map[car.transmission],
        "Owner":        car.owner,
    }])

    predicted_price = float(model.predict(input_df)[0])
    depreciation    = car.present_price - predicted_price
    depreciation_pct = (depreciation / car.present_price * 100) if car.present_price > 0 else 0
    retention_rate  = 100 - depreciation_pct

    return {
        "predicted_price":    round(predicted_price, 2),
        "depreciation":       round(depreciation, 2),
        "depreciation_pct":   round(depreciation_pct, 1),
        "retention_rate":     round(retention_rate, 1),
        "lower_estimate":     round(predicted_price * 0.9, 2),
        "upper_estimate":     round(predicted_price * 1.1, 2),
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
