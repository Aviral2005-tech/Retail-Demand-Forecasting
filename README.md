# AI-Powered Retail Demand Forecasting & Inventory Optimization System

## 📌 Project Overview
Retail businesses often struggle with maintaining optimal inventory levels, leading to either stockouts (lost sales) or overstocking (wasted capital). This project is an end-to-end Machine Learning pipeline that analyzes historical retail sales data, predicts future product demand, and generates actionable inventory recommendations.

## 🚀 Key Features
*   **Exploratory Data Analysis (EDA):** Identifies sales trends, seasonal patterns, and top-performing regions.
*   **Feature Engineering:** Extracts time-series features (day of week, month, weekends) and encodes categorical variables.
*   **Machine Learning Models:** Compares Linear Regression, Random Forest, and Gradient Boosting to accurately forecast unit demand.
*   **Inventory Optimization Engine:** Business logic that calculates safety stock, reorder quantities, and categorizes stock risk.
*   **FastAPI Backend:** A robust, production-ready API to serve real-time predictions.
*   **Streamlit Dashboard:** An interactive web frontend for business users to simulate scenarios and view recommendations.

## 🛠️ Technology Stack
*   **Data Science:** Python, Pandas, NumPy, Scikit-Learn
*   **Machine Learning:** Random Forest Regressor (Best performing model)
*   **Deployment:** FastAPI, Uvicorn, Streamlit
*   **Tools:** Jupyter Notebook, Git

## 📂 Project Structure
```text
Retail-Demand-Forecasting/
│
├── data/
│   ├── raw/                 # Original sales_data.csv
│   └── processed/           # Cleaned and ML-ready datasets
├── notebooks/
│   └── capstone_project.ipynb # Full EDA and model training pipeline
├── models/                  # Serialized Joblib models
├── results/                 # Metrics and sample recommendations
├── deployment/
│   ├── api.py               # FastAPI backend
│   └── dashboard.py         # Streamlit frontend
├── README.md
└── requirements.txt

⚙️ How to Run Locally
1. Clone the repository and install dependencies:

Bash
git clone [https://github.com/your-username/Retail-Demand-Forecasting.git](https://github.com/your-username/Retail-Demand-Forecasting.git)
cd Retail-Demand-Forecasting
pip install -r requirements.txt
2. Start the FastAPI Backend:
Open a terminal and run:

Bash
uvicorn deployment.api:app --reload
The API will be available at http://127.0.0.1:8000

3. Start the Streamlit Dashboard:
Open a second terminal and run:

Bash
streamlit run deployment/dashboard.py
The dashboard will automatically open in your browser.