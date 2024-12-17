import os
import pickle
import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu

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
    
    # Add a download button for the example file
    st.subheader("📂 Download Example Patient Data")
    example_file_path = "example_patient_data.xlsx"

    if os.path.exists(example_file_path):
        with open(example_file_path, 'rb') as file:
            st.download_button(
                label="Download Example Data",
                data=file,
                file_name="example_patient_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
    else:
        st.error("❌ The example data file is missing. Please ensure 'example_patient_data.xlsx' is in the project directory.")
    
    # File upload section
    st.subheader("📂 Upload Your Patient Data")
    uploaded_file = st.file_uploader("Upload a CSV/Excel file with patient data:", type=["csv", "xlsx"])

    # Load the model
    heart_disease_model = None

    model_path = 'saved_models/heart_disease_model.sav'
    if os.path.exists(model_path):
        try:
            with open(model_path, 'rb') as model_file:
                heart_disease_model = pickle.load(model_file)
            st.success("✅ Model loaded successfully! You can now upload your data for prediction.")
        except Exception as e:
            st.error(f"⚠️ Error loading model: {e}")
    else:
        st.error(f"❌ Model file is missing! Ensure '{model_path}' is uploaded.")

    if uploaded_file and heart_disease_model:
        try:
            # Handle file upload
            if uploaded_file.name.endswith('.csv'):
                data = pd.read_csv(uploaded_file)
            else:
                data = pd.read_excel(uploaded_file)

            # Display uploaded data
            st.subheader("🔢 Uploaded Data")
            st.write(data.head())

            # Make predictions
            if st.button("Predict Heart Disease"):
                predictions = heart_disease_model.predict(data)
                data['Prediction'] = predictions
                st.subheader("🔍 Predictions")
                st.write(data)
                
                # Visualize predictions
                fig = px.histogram(data, x='Prediction', title="Heart Disease Predictions", labels={'x': 'Prediction'}, text_auto=True)
                st.plotly_chart(fig)
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
