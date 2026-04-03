# Churn Prediction

Real-time churn risk scoring powered by machine learning. Identify at-risk customers, understand behavior drivers, and take targeted retention actions before it's too late.

## Overview
This project provides an interactive dashboard built with **Streamlit** that utilizes an advanced **XGBoost** machine learning model to predict SaaS customer churn. It analyzes various customer metrics to provide actionable insights for customer retention.

## Technologies Used
- **Python 3.x**
- **Streamlit** (Web Dashboard)
- **Scikit-Learn** & **XGBoost** (Predictive Modeling)
- **Pandas** & **NumPy** (Data manipulation)
- **Plotly** (Interactive Data Visualizations)

## Repository Structure
- `app.py`: Main Streamlit application providing the web interface and real-time inference.
- `churn_model.pkl`: Pre-trained predictive machine learning model (XGBoost).
- `test_predict.py`: Validation script for testing the predictive model's inferences and inputs.
- [requirements.txt](file:///c:/Users/Bhavesh/Downloads/doc-intelligence-platform/doc-intelligence/requirements.txt): Python dependencies required to run the project.

## Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Naikbhavesh123/chrun-pred.git
   cd chrun-pred
   ```

2. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit application:**
   ```bash
   streamlit run app.py
   ```

4. **Verify model predictions:**
   ```bash
   python test_predict.py
   ```

