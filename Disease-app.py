import os
import pickle
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set Page Configuration
st.set_page_config(page_title="Liver and Heart Disease Prediction", layout="wide", page_icon="🏥")

# Function to Load Models
def load_model(model_path):
    try:
        with open(model_path, 'rb') as file:
            return pickle.load(file)
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

# Load heart and liver disease models
heart_disease_model = load_model(r'C:\Users\Sohail\Desktop\final project\heart_disease_model (2).sav')
liver_disease_model = load_model(r'C:\Users\Sohail\Desktop\final project\liver_disease_model (1).sav')

# Sidebar Menu
with st.sidebar:
    selected = option_menu(
        'Multiple Disease Prediction System',
        ['Heart Disease Prediction', 'Liver Disease Prediction', 'Exploratory Data Analysis', 'Plots and Charts', 'Histogram Marker'],
        menu_icon='hospital-fill',
        icons=['heart', 'activity', 'bar-chart', 'bar-chart', 'graph-up'],
        default_index=0
    )

# Heart Disease Prediction
if selected == 'Heart Disease Prediction':
    st.title('Heart Disease Prediction using ML')

    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input('Age', 1, 120, step=1)
        trestbps = st.number_input('Resting Blood Pressure', 50, 250, step=1)
        restecg = st.number_input('Resting ECG (0, 1, 2)', 0, 2, step=1)
        oldpeak = st.number_input('ST Depression', 0.0, step=0.1)
    with col2:
        sex = st.selectbox('Sex', ['Male', 'Female'])
        cp = st.number_input('Chest Pain Type (0-3)', 0, 3, step=1)
        chol = st.number_input('Serum Cholesterol', 100, 600, step=1)
        thalach = st.number_input('Maximum Heart Rate', 60, 220, step=1)
    with col3:
        fbs = st.selectbox('Fasting Blood Sugar > 120 mg/dl (1 = Yes, 0 = No)', [0, 1])
        exang = st.selectbox('Exercise Induced Angina (1 = Yes, 0 = No)', [0, 1])
        slope = st.number_input('Slope of Peak Exercise ST Segment (0, 1, 2)', 0, 2, step=1)

    if st.button('Heart Disease Test Result'):
        sex_num = 1 if sex == 'Male' else 0
        user_input = [age, sex_num, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope]

        if heart_disease_model:
            try:
                prediction = heart_disease_model.predict([user_input])
                result = 'The person has heart disease' if prediction[0] == 1 else 'The person does not have heart disease'
                st.success(result)

                probability = heart_disease_model.predict_proba([user_input])[0][1]
                percentage = round(probability * 100, 2)

                if probability >= 0.7:
                    risk_level = "High Risk ⚠️"
                elif probability >= 0.4:
                    risk_level = "Moderate Risk ⚠️"
                else:
                    risk_level = "Low Risk ✅"

                st.success(f"Probability of Heart Disease: {percentage}%")
                st.info(f"Risk Level: {risk_level}")
            except Exception as e:
                st.error(f"Prediction Error: {e}")
        else:
            st.error("Heart disease model not loaded correctly!")

# Liver Disease Prediction
elif selected == 'Liver Disease Prediction':
    st.title('Liver Disease Prediction using ML')

    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input('Age', 1, 120, step=1)
        BMI = st.number_input('Body Mass Index', 10.0, step=0.1)
        Alcoholcons = st.number_input('Alcohol Consumption', 0.0, step=0.1)
    with col2:
        gender = st.selectbox('Gender', ['Male', 'Female'])
        Smoking = st.selectbox('Smoking (1 = Yes, 0 = No)', [0, 1])
        Genetic_Risk = st.selectbox('Genetic Risk (1 = Yes, 0 = No)', [0, 1])
    with col3:
        PhysicalActivity = st.number_input('Physical Activity', 0.0, step=0.1)
        Diabetes = st.selectbox('Diabetes (1 = Yes, 0 = No)', [0, 1])
        Hypertension = st.selectbox('Hypertension (1 = Yes, 0 = No)', [0, 1])
        liverfunctiontest = st.number_input('Liver Function Test', 0.0, step=0.1)

    Diagnosis = st.selectbox('Diagnosis (0, 1, 2)', [0, 1, 2])

    if st.button('Liver Disease Test Result'):
        gender_num = 1 if gender == 'Male' else 0
        user_input = [age, gender_num, BMI, Alcoholcons, Smoking, Genetic_Risk, PhysicalActivity, Diabetes, Hypertension, liverfunctiontest, Diagnosis]

        if liver_disease_model:
            try:
                prediction = liver_disease_model.predict([user_input])
                result = 'The person has liver disease' if prediction[0] == 1 else 'The person does not have liver disease'
                st.success(result)

                probability = liver_disease_model.predict_proba([user_input])[0][1]
                percentage = round(probability * 100, 2)

                if probability >= 0.7:
                    risk_level = "High Risk ⚠️"
                elif probability >= 0.4:
                    risk_level = "Moderate Risk ⚠️"
                else:
                    risk_level = "Low Risk ✅"

                st.success(f"Probability of Liver Disease: {percentage}%")
                st.info(f"Risk Level: {risk_level}")
            except Exception as e:
                st.error(f"Prediction Error for Liver Disease: {e}")
        else:
            st.error("Liver disease model not loaded correctly!")

# Exploratory Data Analysis
elif selected == "Exploratory Data Analysis":
    st.title("Exploratory Data Analysis")
    dataset_choice = st.selectbox("Select Dataset", ["Heart Disease", "Liver Disease"])
    data_path = (r'C:\Users\Sohail\Desktop\final project\heart (1).csv' if dataset_choice == "Heart Disease" else r'C:\Users\Sohail\Desktop\final project\Liver_disease_data.csv')

    if os.path.exists(data_path):
        data = pd.read_csv(data_path)
        st.write("### Data Preview:")
        st.dataframe(data.head())
        st.write("### Summary Statistics:")
        st.write(data.describe())
        st.write("### Missing Values:")
        st.write(data.isnull().sum())
    else:
        st.error("Dataset not found! Please check the path: " + data_path)

# Plots and Charts
elif selected == "Plots and Charts":
    st.title("Plots and Charts")
    dataset_choice = st.selectbox("Select Dataset", ["Heart Disease", "Liver Disease"])
    data_path = (r'C:\Users\Sohail\Desktop\final project\heart (1).csv' if dataset_choice == "Heart Disease" else r'C:\Users\Sohail\Desktop\final project\Liver_disease_data.csv')

    if os.path.exists(data_path):
        data = pd.read_csv(data_path)
        numeric_cols = data.select_dtypes(include=['int64', 'float64']).columns.tolist()

        if numeric_cols:
            st.write("### Histogram")
            selected_hist_col = st.selectbox("Select column for Histogram", numeric_cols, key='hist_col')
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.histplot(data[selected_hist_col], kde=True, bins=30, ax=ax)
            ax.set_title(f'Histogram of {selected_hist_col}')
            st.pyplot(fig)

            st.write("### Correlation Heatmap")
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.heatmap(data.corr(numeric_only=True), annot=True, cmap='coolwarm', fmt='.2f', ax=ax)
            st.pyplot(fig)

            st.write("### Line Plot")
            x_axis = st.selectbox("Select X-axis", numeric_cols, key='line_x')
            y_axis = st.selectbox("Select Y-axis", numeric_cols, key='line_y')
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.lineplot(x=data[x_axis], y=data[y_axis], marker='o', ax=ax)
            ax.set_title(f'Line Plot of {y_axis} vs {x_axis}')
            st.pyplot(fig)

            st.write("### Box Plot")
            selected_box_col = st.selectbox("Select column for Box Plot", numeric_cols, key='box_col')
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.boxplot(x=data[selected_box_col], ax=ax)
            ax.set_title(f'Box Plot of {selected_box_col}')
            st.pyplot(fig)
        else:
            st.warning("No numeric columns found in dataset.")
    else:
        st.error("Dataset not found! Please check the path: " + data_path)

# Histogram Marker
elif selected == "Histogram Marker":
    st.title("Histogram Marker Tool")
    dataset_choice = st.selectbox("Select Dataset", ["Heart Disease", "Liver Disease"], key="marker_dataset")
    data_path = (r'C:\Users\Sohail\Desktop\final project\heart (1).csv' if dataset_choice == "Heart Disease" else r'C:\Users\Sohail\Desktop\final project\Liver_disease_data.csv')

    if os.path.exists(data_path):
        data = pd.read_csv(data_path)
        numeric_cols = data.select_dtypes(include=['int64', 'float64']).columns.tolist()

        if numeric_cols:
            selected_col = st.selectbox("Select Column for Histogram", numeric_cols)
            marker_value = st.number_input(f"Enter a value to mark on the histogram of {selected_col}", value=float(data[selected_col].mean()))
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.histplot(data[selected_col], bins=30, kde=True, ax=ax)
            ax.axvline(marker_value, color='red', linestyle='--', linewidth=2, label=f'Marked Value: {marker_value}')
            ax.set_title(f"Histogram of {selected_col} with Marker")
            ax.legend()
            st.pyplot(fig)
        else:
            st.warning("No numeric columns found in dataset.")
    else:
        st.error("Dataset not found! Please check the path.")
