import os
import pickle
import streamlit as st
import pandas as pd
import requests
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns
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
                           ['Home', 'About', 'Heart Disease Prediction'],
                           menu_icon='hospital-fill',
                           icons=['house', 'info-circle', 'heart'],
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

# Home Page
if selected == 'Home':
    st.title("Welcome to Heart Disease Prediction System")
    st.markdown("""
    This application uses machine learning to predict whether a person is at risk of heart disease based on various health metrics.
    You can either input your details directly or upload a file with heart disease data for prediction.
    - Use the **Heart Disease Prediction** tab to input your details and get a prediction.
    - Use the **Upload a file** option to predict heart disease for multiple entries at once.
    """)
    st.image("https://www.w3schools.com/w3images/heart.jpg", use_column_width=True)

# About Page
if selected == 'About':
    st.title("About this Project")

    # Project Description
    st.header("Overview")
    st.markdown("""
    This web application is a **Heart Disease Prediction System** built using **Streamlit** and machine learning algorithms. The model predicts whether a person is at risk of heart disease based on health parameters like age, cholesterol levels, and maximum heart rate.

    ### Key Features:
    - **Heart Disease Prediction**: Predict whether a person is at risk of heart disease.
    - **Bulk Predictions**: Upload a CSV/Excel file to predict heart disease for multiple entries at once.
    - **Correlation Visualization**: A heatmap to visualize the correlation between different health features.
    
    ## Technology Stack:
    - **Streamlit**: For building the interactive web interface.
    - **Scikit-learn**: For creating and training the heart disease prediction model.
    - **Matplotlib & Seaborn**: For creating visualizations (like heatmaps).
    """)
    
    # About Us Section
    st.header("About Us")
    st.markdown("""
    We are a team of data science enthusiasts and health experts aiming to leverage the power of machine learning to provide solutions in the medical field. Our goal is to make healthcare predictions more accessible and accurate.

    ### Our Mission:
    Our mission is to provide an easy-to-use platform for heart disease prediction that can help individuals assess their risk and make informed health decisions.

    ### Meet Our Team:
    - **Harshit Suru**: Data Scientist, Machine Learning Specialist
    - **John Doe**: Health Consultant, Cardiologist
    - **Jane Smith**: Frontend Developer, UI/UX Designer

    Feel free to reach out to us at [email@domain.com](mailto:email@domain.com).

    ### Project Link:
    [GitHub Repository](https://github.com/HarshitSuru/HeartDiseasePrediction)
    """)
    st.image("https://www.w3schools.com/w3images/team.jpg", caption="Our Team", use_column_width=True)

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

                    # Visualize results
                    st.subheader("Correlation Heatmap")
                    corr = data.corr()
                    plt.figure(figsize=(12, 8))
                    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
                    st.pyplot()

            except Exception as e:
                st.error(f"Error during prediction: {e}")
        else:
            st.error("Model could not be loaded. Please try again.")
    
    # When no file is uploaded, prediction from input fields
    if uploaded_file is None:
        # Ensure all inputs are numeric
        user_input = [
            float(age), float(sex), float(cp), float(trestbps), float(chol), float(fbs),
            float(restecg), float(thalach), float(exang), float(oldpeak), float(slope), 
            float(ca), float(thal)
        ]
        
        # Create a button for prediction
        if st.button('Predict Heart Disease'):
            # Validate input
            if heart_disease_model:
                try:
                    # Get prediction based on the user's input
                    prediction = heart_disease_model.predict([user_input])
                    if prediction[0] == 1:
                        st.success("The person is at risk of heart disease.")
                    else:
                        st.success("The person does not have heart disease.")
                except Exception as e:
                    st.error(f"Error during prediction: {e}")
            else:
                st.error("Model is not loaded properly. Please try again.")
