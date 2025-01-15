# -*- coding: utf-8 -*-
"""Untitled4.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Vh8UnH5jwYnGsJKEebtp_JnFtJBJoZa0
"""

import streamlit as st

from google.colab import drive
drive.mount('/content/drive')

import streamlit as st  # Pastikan Streamlit diimpor
import pandas as pd

# Cache untuk mempercepat proses pemuatan data
@st.cache
def load_data():
    data = pd.read_csv('/content/drive/MyDrive/meachin learning/baru/performa siswa/Student_Performance (6).csv')
    return data

data = load_data()

# Streamlit UI
st.title("Student Performance Prediction")

# Display basic info about the dataset
st.subheader("Dataset Overview")
st.write(data.head())
st.write("Dataset Shape:", data.shape)
st.write("Missing values:", data.isna().sum())

# Sidebar for navigation
option = st.sidebar.selectbox(
    "Choose a model",
    ["Linear Regression", "Random Forest"]
)

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Preprocessing for Model
encoder = LabelEncoder()
data["Extracurricular Activities"] = encoder.fit_transform(data["Extracurricular Activities"])

Train = data.drop(columns="Performance Index")
Target = data["Performance Index"]

X_train, X_test, y_train, y_test = train_test_split(Train, Target, test_size=0.2, random_state=42)

from sklearn.linear_model import LinearRegression  # Tambahkan ini

# Model Selection
if option == "Linear Regression":
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

from sklearn.metrics import mean_absolute_error, r2_score
st.subheader("Linear Regression Results")
st.write("Mean Absolute Error:", mean_absolute_error(y_test, y_pred))
st.write("R^2 Score:", r2_score(y_test, y_pred))
st.subheader("Predicted vs Actual Values")
comparison = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
st.write(comparison)

if option == "Random Forest":
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred_rf = model.predict(X_test)

    st.subheader("Random Forest Results")
    st.write("Mean Absolute Error:", mean_absolute_error(y_test, y_pred_rf))
    st.write("R^2 Score:", r2_score(y_test, y_pred_rf))

    st.subheader("Predicted vs Actual Values")
    comparison_rf = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred_rf})
    st.write(comparison_rf)

    st.subheader("Feature Importance")
    feature_importance = model.feature_importances_
    features = Train.columns
    importance_df = pd.DataFrame({'Feature': features, 'Importance': feature_importance})
    st.write(importance_df)

import matplotlib.pyplot as plt
import seaborn as sns

# Visualization in Streamlit
st.subheader("Correlation Heatmap")
plt.figure(figsize=(10, 6))
sns.heatmap(data.select_dtypes(exclude="object").corr(), annot=True, fmt=".2f", cmap='coolwarm')
st.pyplot(plt)  # Gunakan plt sebagai parameter untuk Streamlit