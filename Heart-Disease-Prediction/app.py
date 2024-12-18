import os
import pickle
import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
import requests

# Set page configuration
st.set_page_config(
    page_title="Health Assistant - Heart Disease Prediction",
    layout="wide",
    page_icon="🧑‍⚕️",
)

# Sidebar navigation
with st.sidebar:
    selected = option_menu(
        "Health Assistant",
        ["Home", "Heart Disease Prediction", "About Us"],
        icons=["house", "heart", "info-circle"],
        menu_icon="activity",  
        default_index=0,
        styles={
            "container": {"padding": "2px", "background-color": "#34495E"},
            "icon": {"color": "#F39C12", "font-size": "18px"},  
            "nav-link": {"font-size": "14px", "text-align": "center", "margin": "3px", "--hover-color": "#F39C12"},
            "nav-link-selected": {"background-color": "#F39C12"},
        }
    )

# Home page
if selected == "Home":
    st.title("🧑‍⚕️ Welcome to Health Assistant")
    st.markdown(
        """
        ### 🌟 About This Application
        The Health Assistant uses a machine learning model to predict the likelihood of heart disease 
        based on various health indicators.

        ### 🔉 Important
        This tool provides **preliminary insights** only. Always consult a healthcare provider for a proper diagnosis.

        ### ❤️ What is Heart Disease?
        Heart disease refers to conditions affecting the heart, including coronary artery disease and others. Common causes include high blood pressure, high cholesterol, and smoking.

        #### Preventive Measures:
        - Healthy diet
        - Regular exercise
        - Avoid smoking and excessive alcohol
        - Monitor blood pressure, cholesterol, and sugar levels
        - Manage stress

        ### 📈 Prediction Insights
        This app assesses the likelihood of heart disease. Follow up with a healthcare provider for diagnostic tests if needed.
        """
    )

# Heart Disease Prediction page
if selected == "Heart Disease Prediction":
    st.title("🧬 Heart Disease Prediction")
    st.markdown(
        """
        **Upload patient data** to predict the likelihood of heart disease.

        ### 🔓 How to Use:
        1. **Download the example data** below.
        2. **Upload your own data** in CSV or Excel format.
        3. Click **Predict Heart Disease** to generate predictions.
        """
    )
    
    # Add a download button for the example file
    example_file_url = "https://github.com/HarshitSuru/HeartDiseasePrediction/raw/main/Heart-Disease-Prediction/example_patient_data.xlsx"
    try:
        response = requests.get(example_file_url)
        if response.status_code == 200:
            st.download_button(
                label="Download Example Data",
                data=response.content,
                file_name="example_patient_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        else:
            st.error("❌ Failed to download example data from GitHub.")
    except Exception as e:
        st.error(f"⚠️ Error downloading example data: {e}")
    
    # File upload section
    uploaded_file = st.file_uploader("Upload a CSV/Excel file with patient data:", type=["csv", "xlsx"])

    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                data = pd.read_csv(uploaded_file)
            else:
                data = pd.read_excel(uploaded_file)

            required_columns = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
            missing_columns = [col for col in required_columns if col not in data.columns]

            if missing_columns:
                st.error(f"⚠️ The uploaded file is missing: {', '.join(missing_columns)}")
            else:
                st.subheader("🔢 Uploaded Data")
                st.write(data.head())
                
                # Visualizations
                st.subheader("📊 Data Analysis & Visualizations")
                st.plotly_chart(px.histogram(data, x='age', title="Age Distribution", labels={'age': 'Age'}))
                st.plotly_chart(px.histogram(data, x='chol', title="Cholesterol Levels Distribution", labels={'chol': 'Cholesterol Level'}))
                st.plotly_chart(px.pie(data, names='sex', title="Sex Distribution", hole=0.3))

        except Exception as e:
            st.error(f"⚠️ Error processing file: {e}")

    # Load model
    model_url = "https://github.com/HarshitSuru/HeartDiseasePrediction/raw/main/Heart-Disease-Prediction/saved_models/heart_disease_model.sav"
    try:
        response = requests.get(model_url)
        if response.status_code == 200:
            with open("heart_disease_model.sav", "wb") as model_file:
                model_file.write(response.content)
            with open("heart_disease_model.sav", "rb") as model_file:
                heart_disease_model = pickle.load(model_file)
            st.success("✅ Model loaded successfully! You can now proceed with predictions.")
        else:
            st.error("❌ Failed to download model file from GitHub.")
    except Exception as e:
        st.error(f"⚠️ Error loading model: {e}")

    if uploaded_file and 'heart_disease_model' in locals() and not missing_columns:
        try:
            data = data[required_columns]
            if st.button("Predict Heart Disease"):
                predictions = heart_disease_model.predict(data)
                st.subheader("🩺 Prediction Results")
                st.write(predictions)
                st.markdown(
                    """
                    ### Interpretation of Results:
                    - **1**: High likelihood of heart disease.
                    - **0**: Low likelihood of heart disease.

                    #### Next Steps:
                    - If positive, consult a healthcare provider immediately.
                    - This tool is for guidance only, not a substitute for medical advice.
                    """
                )
        except Exception as e:
            st.error(f"⚠️ Error during prediction: {e}")
# About Us page
if selected == "About Us":
    st.title("👨‍💼 About Us")
    st.markdown(
        """
        ### Our Mission:
        We aim to leverage technology for better health outcomes by providing easy-to-use tools for health analysis.

        #### Contact:
        - **GitHub**: [HarshitSuru](https://github.com/HarshitSuru/)
        - **LinkedIn**: [Harshit Suru](https://www.linkedin.com/in/suru-harshit-4863372bb)
        - **Email**: [suruharshit2005@gmail.com](mailto:suruharshit2005@gmail.com)

        #### Disclaimer:
        - This application is a supportive tool, not a diagnostic device. Always consult medical professionals for health concerns.
        """
    )

