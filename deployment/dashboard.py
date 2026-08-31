import streamlit as st
import requests
from datetime import datetime

# Set up the page layout
st.set_page_config(page_title="Retail Demand Forecaster", layout="wide")

st.title("📊 Retail Demand Forecasting & Inventory Optimization")
st.markdown("Predict future product demand and optimize your inventory levels using Machine Learning.")

# Sidebar for user inputs
st.sidebar.header("Input Parameters")
    
input_date = st.sidebar.date_input("Forecast Date", datetime.today())
product = st.sidebar.selectbox("Product", ["Product A", "Product B", "Product C"]) 
region = st.sidebar.selectbox("Region", ["North", "South", "East", "West"]) 
price = st.sidebar.number_input("Price ($)", min_value=0.0, value=120.0, step=10.0)
current_inventory = st.sidebar.number_input("Current Inventory", min_value=0, value=80, step=1)

if st.sidebar.button("Predict Demand & Optimize"):
    # Prepare the JSON payload for the FastAPI backend
    payload = {
        "date": input_date.strftime("%Y-%m-%d"),
        "product": product,
        "region": region,
        "price": price,
        "current_inventory": current_inventory
    }
        
    try:
        # Make the POST request to the local FastAPI server
        response = requests.post("http://127.0.0.1:8000/predict", json=payload)
            
        if response.status_code == 200:
            result = response.json()
                
            st.subheader("Inventory Recommendations")
                
            # Display key metrics in columns
            col1, col2, col3 = st.columns(3)
            col1.metric("Predicted Demand", result["Predicted_Demand"])
            col2.metric("Target Inventory", result["Target_Inventory"])
            col3.metric("Reorder Quantity", result["Reorder_Quantity"])
                
            # Display Risk Level with dynamic color coding
            risk = result["Stock_Risk"]
            if "HIGH" in risk:
                st.error(f"⚠️ Risk Level: {risk}")
            elif "MODERATE" in risk:
                st.warning(f"⚠️ Risk Level: {risk}")
            elif "OVERSTOCK" in risk:
                st.info(f"ℹ️ Risk Level: {risk}")
            else:
                st.success(f"✅ Risk Level: {risk}")
                    
        else:
            st.error(f"Error from API: {response.text}")
                
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to the backend API. Is the FastAPI server running?")