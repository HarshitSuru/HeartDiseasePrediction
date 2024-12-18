import os
import pickle
import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from streamlit_option_menu import option_menu

# Set page configuration
st.set_page_config(page_title="Heart Disease Prediction",
                   layout="wide",
                   page_icon="❤️")

# Sidebar navigation styles
sidebar_style = """
    <style>
        .css-18e3th9 {padding: 0;}
        .css-1d391kg {padding: 1rem;}
        .css-1kpfpqw {padding: 1rem;}
        .css-1y4g43s {text-align: center;}
    </style>
"""
st.markdown(sidebar_style, unsafe_allow_html=True)

# Sidebar for navigation
with st.sidebar:
    selected = option_menu('Heart Disease Prediction System',
                           ['Heart Disease Prediction'],
                           menu_icon='hospital-fill',
                           icons=['heart'],
                           default_index=0,
                           styles={
                               "container": {"padding": "2px", "background-color": "#34495E"},
                               "icon": {"color": "#F39C12", "font-size": "18px"},
                               "nav-link": {"font-size": "14px", "text-align": "center", "margin": "3px", "--hover-color": "#F39C12"},
                               "nav-link-selected": {"background-color": "#F39C12"},
                           })

# Function to download model from GitHub
def download_model():
    model_url = "https://github.com/HarshitSuru/HeartDiseasePrediction/raw/main/Heart-Disease-Prediction/saved_models/heart_disease_model.sav"
    response = requests.get(model_url)
    if response.status_code == 200:
        model = pickle.load(BytesIO(response.content))
        return model
    else:
        st.error("Failed to download model from GitHub.")
        return None

# Download the model
heart_disease_model = download_model()

# Function to handle predictions
def get_predictions(model, user_input):
    return model.predict([user_input])

# Heart Disease Prediction Page
if selected == 'Heart Disease Prediction':
    st.title('Heart Disease Prediction using ML')

    # Get input data from user
    col1, col2, col3 = st.columns(3)
    with col1: age = st.text_input('Age')
    with col2: sex = st.text_input('Sex')
    with col3: cp = st.text_input('Chest Pain types')
    with col1: trestbps = st.text_input('Resting Blood Pressure')
    with col2: chol = st.text_input('Serum Cholestoral in mg/dl')
    with col3: fbs = st.text_input('Fasting Blood Sugar > 120 mg/dl')
    with col1: restecg = st.text_input('Resting Electrocardiographic results')
    with col2: thalach = st.text_input('Maximum Heart Rate achieved')
    with col3: exang = st.text_input('Exercise Induced Angina')
    with col1: oldpeak = st.text_input('ST depression induced by exercise')
    with col2: slope = st.text_input('Slope of the peak exercise ST segment')
    with col3: ca = st.text_input('Major vessels colored by fluoroscopy')
    with col1: thal = st.text_input('thal: 0 = normal; 1 = fixed defect; 2 = reversible defect')

    # File upload section for the user to upload their own data
    uploaded_file = st.file_uploader("Upload a CSV or Excel file with heart disease data:", type=["csv", "xlsx"])

    if uploaded_file is not None:
        # Read the uploaded file into a DataFrame
        if uploaded_file.name.endswith(".csv"):
            data = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".xlsx"):
            data = pd.read_excel(uploaded_file)

        # Display uploaded data
        st.subheader("Uploaded Data")
        st.write(data)

        # Predict based on the uploaded data
        if heart_disease_model:
            try:
                # Make sure the necessary columns exist
                required_columns = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
                missing_columns = [col for col in required_columns if col not in data.columns]

                if missing_columns:
                    st.error(f"Missing columns in the uploaded data: {', '.join(missing_columns)}")
                else:
                    # Predict heart disease for each row
                    predictions = heart_disease_model.predict(data[required_columns])
                    data['Heart Disease Prediction'] = predictions

                    # Display results
                    st.subheader("Prediction Results")
                    st.write(data)

            except Exception as e:
                st.error(f"Error during prediction: {e}")
        else:
            st.error("Model could not be loaded. Please try again.")
