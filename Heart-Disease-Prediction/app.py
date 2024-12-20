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

# Sidebar navigation with modern design
with st.sidebar:
    st.markdown("""<style>
        .css-1cpxqw2 a {
            font-size: 14px !important;
            font-weight: 600 !important;
            color: #ffffff !important;
        }
        .css-1cpxqw2 a:hover {
            color: #F39C12 !important;
        }
        .css-1cpxqw2 .nav-link {
            border-radius: 8px !important;
            margin: 4px 0;
            padding: 6px 10px !important;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .css-1cpxqw2 .nav-link:hover {
            background-color: #F39C12 !important;
            color: #ffffff !important;
        }
    </style>""", unsafe_allow_html=True)
    
    selected = option_menu(
        "Health Assistant",
        ["Home", "Heart Disease Prediction", "About Us"],
        icons=["house", "heart", "info-circle"],
        menu_icon="activity",  
        default_index=0,
        orientation="vertical",
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
        based on various health indicators (e.g., age, cholesterol, blood pressure). 
        It provides insights for individuals and healthcare professionals.

        ### 🔉 Important
        This tool provides **preliminary insights** only. It is **not** a substitute for professional medical advice. Always consult a healthcare provider for a proper diagnosis.
        """
    )

# Heart Disease Prediction page
if selected == "Heart Disease Prediction":
    st.title("🧬 Heart Disease Prediction")
    st.markdown(
        """
        **Upload patient data** to predict the likelihood of heart disease and receive advice on next steps.

        ### 🔓 How to Use:
        1. **Download the example data** (provided below) to see the required format for your input file.
        2. **Upload your own data** in CSV or Excel format.
        3. Click **Predict Heart Disease** to generate predictions.
        4. View the results and get tips based on predictions.
        """
    )
    
    # Add a download button for the example file from GitHub
    st.subheader("📂 Download Example Patient Data")
    example_file_url = "https://github.com/HarshitSuru/HeartDiseasePrediction/raw/main/Heart-Disease-Prediction/example_patient_data.xlsx"

    try:
        # Download example data file from GitHub
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
    st.subheader("📂 Upload Your Patient Data")
    uploaded_file = st.file_uploader("Upload a CSV/Excel file with patient data:", type=["csv", "xlsx"])

    if uploaded_file:
        try:
            # Check and display file structure
            if uploaded_file.name.endswith('.csv'):
                data = pd.read_csv(uploaded_file)
            else:
                data = pd.read_excel(uploaded_file)

            required_columns = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
            missing_columns = [col for col in required_columns if col not in data.columns]

            if missing_columns:
                st.error(f"⚠️ The uploaded file is missing the following required columns: {', '.join(missing_columns)}")
            else:
                # Display the first few rows of the data
                st.subheader("🔢 Uploaded Data")
                st.write(data.head())
                
                # Ensure all rows are considered, and drop extra columns
                data = data[required_columns]

                # Load the model from GitHub
                heart_disease_model = None
                model_url = "https://github.com/HarshitSuru/HeartDiseasePrediction/raw/main/Heart-Disease-Prediction/saved_models/heart_disease_model.sav"

                try:
                    # Download model file from GitHub
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

                if heart_disease_model:
                    try:
                        # Make predictions on all rows of data
                        if st.button("Predict Heart Disease"):
                            predictions = heart_disease_model.predict(data)
                            data['Prediction'] = predictions
                            st.subheader("🔍 Predictions")
                            st.write(data)
                            
                            # Visualize predictions
                            fig = px.histogram(data, x='Prediction', title="Heart Disease Predictions", labels={'x': 'Prediction'}, text_auto=True)
                            st.plotly_chart(fig)
                    except Exception as e:
                        st.error(f"⚠️ Error during prediction: {e}")
        except Exception as e:
            st.error(f"⚠️ Error processing file: {e}")

# About Us page
if selected == "About Us":
    st.title("👨‍💼 About Us")
    st.markdown(
        """
        ### We aim to harness technology for better health management.

        #### Connect with the Developer:
        - [GitHub](https://github.com/HarshitSuru/)
        - [LinkedIn](https://www.linkedin.com/in/suru-harshit-4863372bb)
        - Email: [suruharshit2005@gmail.com](mailto:suruharshit2005@gmail.com)
        """
    )
