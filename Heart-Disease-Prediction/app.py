import os
import pickle
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu

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
    )

# Home page
if selected == "Home":
    st.title("🧑‍⚕️ Health Assistant")
    st.write("Welcome to the Health Assistant application! This tool is designed to help you assess heart disease risk based on input data.")
    
    st.subheader("🌟 About This Application")
    st.write(
        "The Health Assistant uses a machine learning model to predict the likelihood of heart disease based on several health indicators, "
        "including age, cholesterol levels, blood pressure, and more. It allows healthcare professionals and individuals to get insights "
        "based on real medical data."
    )

    st.subheader("📝 How to Use")
    st.write(
        """
        1. Navigate to the **Heart Disease Prediction** section using the sidebar.
        2. Upload a CSV or Excel file containing the necessary health information for each patient.
        3. Click on the **Predict Heart Disease** button to generate predictions.
        4. After predictions, you’ll receive tailored advice based on the results.
        """
    )

    st.subheader("💡 Note")
    st.write(
        "This application is a tool for providing preliminary insights and should not be a substitute for professional medical advice. "
        "Always consult a healthcare provider for a comprehensive diagnosis."
    )

# Heart Disease Prediction page
if selected == "Heart Disease Prediction":
    st.title("🧑‍⚕️ Heart Disease Prediction System")
    st.write(
        "This application predicts the likelihood of heart disease based on user input. "
        "Please upload a CSV or Excel file with the relevant information for accurate prediction."
    )

    # File upload
    st.subheader("🔍 Upload Patient Data")
    uploaded_file = st.file_uploader("Upload a CSV/Excel file with patient data:", type=["csv", "xlsx"])

    # Load model
    heart_disease_model = None
    model_path = 'C:/Users/suruh/OneDrive/Desktop/multiple-disease-prediction-streamlit-app-main/multiple-disease-prediction-streamlit-app-main/saved_models/heart_disease_model.sav'

    try:
        # Check if model file exists before loading
        if os.path.exists(model_path):
            heart_disease_model = pickle.load(open(model_path, 'rb'))
            st.success("Model successfully loaded! Please upload a file below to proceed with predictions.")
        else:
            st.error(f"Model file '{model_path}' not found. Please upload the model file.")
    except Exception as e:
        st.error(f"Error loading model: {e}")

    # Only proceed if file is uploaded and model is loaded
    if uploaded_file is not None and heart_disease_model is not None:
        # Read the file based on type (CSV or Excel)
        if uploaded_file.type == "text/csv":
            data = pd.read_csv(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            data = pd.read_excel(uploaded_file)

        st.write("### Data Preview")
        st.dataframe(data)  # Display the entire dataset with interactive scrolling

        # Ensure the file has the required columns
        required_columns = [
            "age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", 
            "thalach", "exang", "oldpeak", "slope", "ca", "thal"
        ]

        # Check if all required columns are present
        if all(col in data.columns for col in required_columns):
            # Prepare the data for prediction (ensure the format matches the model's requirements)
            data_prepared = data[required_columns]

            # Prediction
            if st.button("Predict Heart Disease"):
                try:
                    predictions = heart_disease_model.predict(data_prepared)
                    # Show results
                    st.write("### Predictions")
                    prediction_results = ["Heart Disease" if pred == 1 else "No Heart Disease" for pred in predictions]
                    
                    # Add the prediction results to the dataframe
                    data['Prediction'] = prediction_results
                   # st.write(data)

                    # Separate results into two categories for personalized advice
                    diseased = data[data['Prediction'] == "Heart Disease"]
                    undiseased = data[data['Prediction'] == "No Heart Disease"]

                    # Advice for diseased individuals
                    if not diseased.empty:
                        st.subheader("⚠️ Advice for Individuals with Heart Disease")
                        st.write(
                            """
                            - **Seek Medical Attention**: It's crucial to consult a healthcare provider for further evaluation and treatment.
                            - **Lifestyle Changes**: Focus on a balanced diet, regular exercise, and stress management.
                            - **Medication**: Follow any prescribed medication regimens carefully.
                            - **Regular Check-Ups**: Keep track of your heart health with regular medical visits.
                            """
                        )
                        st.write("Affected Individuals:")
                        st.write(diseased[['age', 'sex', 'chol', 'trestbps', 'thalach', 'Prediction']])

                    # Advice for undiseased individuals
                    if not undiseased.empty:
                        st.subheader("✅ Tips for Maintaining Heart Health")
                        st.write(
                            """
                            - **Healthy Diet**: Eat a diet rich in fruits, vegetables, and whole grains.
                            - **Stay Active**: Aim for at least 30 minutes of moderate physical activity most days.
                            - **Avoid Smoking**: Smoking significantly increases heart disease risk.
                            - **Regular Check-Ups**: Continue to monitor your health, even if you're at low risk.
                            """
                        )
                        st.write("Unaffected Individuals:")
                        st.write(undiseased[['age', 'sex', 'chol', 'trestbps', 'thalach', 'Prediction']])
                except Exception as e:
                    st.error(f"Error during prediction: {e}")
        else:
            st.warning(f"Missing required columns. Ensure your file includes the following columns: {', '.join(required_columns)}")
    else:
        if uploaded_file is None:
            st.info("Please upload a CSV or Excel file to make a prediction.")
        if heart_disease_model is None:
            st.error("Model not loaded. Please check the model path.")

# About Us page
if selected == "About Us":
    st.title("👨‍💻 About Us")
    st.write("This Health Assistant application was developed to assist individuals and professionals in predicting heart disease risks.")

    st.subheader("Connect with Me")
    st.write(
        """
        - [GitHub](https://github.com/HarshitSuru/)
        - [LinkedIn](https://www.linkedin.com/in/suru-harshit-4863372bb)
        - Email: [suruharshit2005@gmail.com](mailto:suruharshit2005@gmail.com)
        """
    )
