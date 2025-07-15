import streamlit as st
import pandas as pd
import numpy as np
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns

# Page config
st.set_page_config(page_title="🏠 House Price Predictor", page_icon="💰", layout="centered")

# Sidebar branding
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/6195/6195700.png", width=100)
    st.markdown("## House Price ML Model")
    st.markdown("Upload your dataset, train a model, and visualize the prediction results.")
    st.markdown("---")

# Title
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🏡 House Price Prediction Dashboard</h1>", unsafe_allow_html=True)

# Upload section
uploaded_file = st.file_uploader("📂 Upload your Housing CSV file", type=['csv', 'xls'])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.markdown("### 🔍 Dataset Preview")
    st.dataframe(df.head(), use_container_width=True)

    # Features
    categorical_features = ['mainroad', 'guestroom', 'basement', 'hotwaterheating',
                            'airconditioning', 'prefarea', 'furnishingstatus']
    X = df.drop('price', axis=1)
    y = df['price']

    # Pipeline
    preprocessor = ColumnTransformer([
        ('onehot', OneHotEncoder(drop='first'), categorical_features)
    ], remainder='passthrough')

    model = Pipeline([
        ('preprocess', preprocessor),
        ('regressor', LinearRegression())
    ])

    # Split and train
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    model.fit(X_train, y_train)

    st.success("✅ Model Trained Successfully!")

    # Predictions
    y_pred = model.predict(X_test)

    # Evaluation
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    # Metrics display
    st.markdown("### 📈 Model Evaluation Metrics")
    col1, col2 = st.columns(2)
    col1.metric("💹 RMSE", f"₹ {rmse:,.2f}")
    col2.metric("📊 R² Score", f"{r2:.4f}")

    # Plot
    st.markdown("### 📉 Actual vs Predicted House Prices")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.set(style="whitegrid")
    sns.scatterplot(x=y_test, y=y_pred, ax=ax, color="#4CAF50", s=80)
    ax.set_xlabel("Actual Price", fontsize=12)
    ax.set_ylabel("Predicted Price", fontsize=12)
    ax.set_title("Actual vs Predicted Prices", fontsize=14, fontweight='bold')
    st.pyplot(fig)

    # Footer
    st.markdown("---")
    st.markdown("<h6 style='text-align:center;'>📌 Tip: The closer the dots are to a diagonal line, the better the model is performing.</h6>", unsafe_allow_html=True)
