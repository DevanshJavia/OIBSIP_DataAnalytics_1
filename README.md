House Price Prediction Web Application with Model Explainability (SHAP)

Objective

To build a machine learning-powered web application that predicts house prices based on user inputs, while providing transparent model explanations using SHAP (SHapley Additive Explanations) to improve trust and interpretability.

Tools & Technologies Used

Programming Language: Python
Machine Learning Libraries:
Pandas, NumPy: Data preprocessing and manipulation
Scikit-learn: Linear Regression, Pipelines, Preprocessing, and Evaluation
SHAP: Model interpretability using SHAP values
Joblib: Saving and loading trained models
Visualization:
Matplotlib, Seaborn: For exploratory and performance plots
Chart.js: For interactive dashboard graphs
Web Development:
Django: Full-stack web framework for integrating frontend and backend
HTML, CSS, Bootstrap: UI and layout design

Workflow / Steps Performed

Data Loading & Cleaning: Imported housing data from a CSV file and processed it.
Feature Engineering: Defined categorical and numerical features.
Model Pipeline:
Used ColumnTransformer and OneHotEncoder for preprocessing.
Applied LinearRegression model using a scikit-learn Pipeline.
Train/Test Split: Divided data to train and evaluate model.
Model Training & Evaluation: Measured performance using Mean Squared Error (MSE) and R-squared (R²).
Model Persistence: Saved the trained pipeline with joblib.
Model Explainability:
Used SHAP to generate feature impact visualizations.
Saved a SHAP beeswarm summary plot.
Web Integration:
Developed a Django app with user login, form-based predictions, and prediction history.
Created an interactive dashboard with line, bar, pie, and monthly charts.
Embedded SHAP plots into the dashboard for explainable AI.

Outcome

Developed a complete end-to-end machine learning web application.
Enabled transparent predictions with model explainability using SHAP.
Delivered a clean and interactive dashboard to monitor prediction history and feature influence.
Final result: A deployable, interpretable, and user-friendly House Price Prediction System.
