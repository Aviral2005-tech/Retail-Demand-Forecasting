from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib
import os
from datetime import datetime

# Initialize the FastAPI app
app = FastAPI(
    title="Retail Demand Forecasting API",
    description="API for predicting product demand and optimizing inventory",
    version="1.0.0"
)

# Define the paths (assuming the app is run from the root project directory)
MODEL_PATH = "models/demand_forecasting_model.joblib"
FEATURES_PATH = "models/model_features.joblib"

# Load the trained model and expected feature columns globally
try:
    model = joblib.load(MODEL_PATH)
    model_features = joblib.load(FEATURES_PATH)
    print("Model and features loaded successfully.")
except Exception as e:
    model = None
    model_features = None
    print(f"Warning: Could not load model files. Error: {e}")

# Define the expected JSON payload format
class PredictionRequest(BaseModel):
    date: str              # Format: YYYY-MM-DD
    product: str           # e.g., "Product A"
    region: str            # e.g., "North"
    price: float           # e.g., 120.0
    current_inventory: int # e.g., 80

def generate_inventory_recommendation(predicted_demand, current_inventory):
    """Business logic for inventory optimization."""
    predicted_demand = max(0, int(predicted_demand))
    safety_stock = int(predicted_demand * 0.20)
    target_inventory = predicted_demand + safety_stock
    reorder_qty = max(0, target_inventory - current_inventory)
    
    if current_inventory < predicted_demand:
        risk_level = "HIGH STOCKOUT RISK"
    elif current_inventory < target_inventory:
        risk_level = "MODERATE RISK"
    elif current_inventory > (target_inventory * 1.5):
        risk_level = "OVERSTOCK RISK (Wasted Capital)"
    else:
        risk_level = "OPTIMAL INVENTORY"
        
    return {
        "Predicted_Demand": predicted_demand,
        "Current_Inventory": current_inventory,
        "Safety_Stock": safety_stock,
        "Target_Inventory": target_inventory,
        "Reorder_Quantity": reorder_qty,
        "Stock_Risk": risk_level
    }

@app.post("/predict")
def predict_demand(request: PredictionRequest):
    if model is None or model_features is None:
        raise HTTPException(status_code=500, detail="Machine Learning model not loaded.")
        
    try:
        # 1. Initialize an empty dictionary with 0s for all expected features
        input_dict = {col: 0 for col in model_features}
        
        # 2. Extract and set Time Features
        date_obj = datetime.strptime(request.date, "%Y-%m-%d")
        input_dict['Price'] = request.price
        input_dict['Month'] = date_obj.month
        input_dict['DayOfWeek'] = date_obj.weekday()
        input_dict['IsWeekend'] = 1 if date_obj.weekday() >= 5 else 0
        
        # 3. Set One-Hot Encoded Categorical Features
        product_col = f"Product_{request.product}"
        if product_col in input_dict:
            input_dict[product_col] = 1
            
        region_col = f"Region_{request.region}"
        if region_col in input_dict:
            input_dict[region_col] = 1
            
        # 4. Convert to DataFrame and predict
        df_input = pd.DataFrame([input_dict])
        prediction = model.predict(df_input)[0]
        
        # 5. Pass prediction to business logic
        recommendation = generate_inventory_recommendation(prediction, request.current_inventory)
        
        return recommendation
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))