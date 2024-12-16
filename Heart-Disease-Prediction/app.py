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
    st.title("🩺 Heart Disease Prediction")
    st.markdown(
        """
        **Upload patient data** to predict the likelihood of heart disease and receive advice on next steps.

        ### 📖 How to Use:
        1. **Download the example data** (provided below) to see the required format for your input file.
        2. **Upload your own data** in CSV or Excel format.
        3. Click **Predict Heart Disease** to generate predictions.
        4. View the results and get tips based on predictions.

        ### 📝 Example Data:
        Download the **example file** with data for 12 individuals. This file contains health attributes that the model uses for predictions:
        
        - **Age**: Individual’s age.
        - **Sex**: Gender (1 = male, 0 = female).
        - **CP (Chest Pain Type)**: Classification of chest pain (0, 1, 2, 3).
        - **Trestbps (Resting Blood Pressure)**: Blood pressure in mm Hg.
        - **Chol (Serum Cholesterol)**: Cholesterol level in mg/dl.
        - **Fbs (Fasting Blood Sugar)**: High fasting blood sugar (1 = true, 0 = false).
        - **Restecg (Resting Electrocardiographic Results)**: Electrocardiogram results (0, 1, 2).
        - **Thalach (Maximum Heart Rate)**: Max heart rate achieved.
        - **Exang (Exercise Induced Angina)**: Angina during exercise (1 = yes, 0 = no).
        - **Oldpeak**: Depression caused by exercise compared to rest.
        - **Slope**: Slope of the peak exercise ST segment (0, 1, 2).
        - **CA**: Number of major vessels colored by fluoroscopy (0-3).
        - **Thal**: Thalassemia type (3 = normal, 6 = fixed defect, 7 = reversible defect).
        - **CDM (Heart Disease)**: Pre-generated prediction (0 = no, 1 = yes).

        ### 📂 Download Example Data
        The file contains data for **12 individuals**. Use this file to see how the model works. After downloading, upload it here to make predictions.

        """
    )

    # Add a download button for the example file
    st.subheader("📂 Download Example Patient Data")
    example_file = 'example_patient_data.xlsx'  # Ensure this file exists in your project directory
    with open(example_file, 'rb') as file:
        st.download_button(
            label="Download Example Data",
            data=file,
            file_name="example_patient_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        
    # File upload section
    st.subheader("📂 Upload Your Patient Data")
    uploaded_file = st.file_uploader("Upload a CSV/Excel file with patient data:", type=["csv", "xlsx"])

    # Load the model
    heart_disease_model = None
    model_path = r'C:\Users\suruh\OneDrive\Desktop\HeartDiseasePrediction\Heart-Disease-Prediction\saved_models\heart_disease_model.sav'

    try:
        if os.path.exists(model_path):
            heart_disease_model = pickle.load(open(model_path, 'rb'))
            st.success("Model loaded successfully! You can now upload your data for prediction.")
        else:
            st.error(f"Model not found at {model_path}")
    except Exception as e:
        st.error(f"Error loading model: {e}")

    # Proceed if file is uploaded and model is loaded
    if uploaded_file is not None and heart_disease_model is not None:
        # Read the file
        try:
            if uploaded_file.type == "text/csv":
                data = pd.read_csv(uploaded_file)
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                data = pd.read_excel(uploaded_file)

            st.write("### Data Preview")
            st.dataframe(data.head())

            # Visualizations (if relevant columns are present)
            st.write("### Data Insights")
            if 'age' in data.columns and 'chol' in data.columns:
                fig = px.histogram(data, x="age", title="Age Distribution", nbins=20, color_discrete_sequence=['teal'])
                st.plotly_chart(fig)

                fig = px.histogram(data, x="chol", title="Cholesterol Level Distribution", nbins=20, color_discrete_sequence=['orange'])
                st.plotly_chart(fig)

            required_columns = [
                "age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", 
                "thalach", "exang", "oldpeak", "slope", "ca", "thal"
            ]

            if all(col in data.columns for col in required_columns):
                data_prepared = data[required_columns]

                if st.button("Predict Heart Disease"):
                    try:
                        predictions = heart_disease_model.predict(data_prepared)
                        data['Prediction'] = ["Heart Disease" if pred == 1 else "No Heart Disease" for pred in predictions]

                        diseased = data[data['Prediction'] == "Heart Disease"]
                        undiseased = data[data['Prediction'] == "No Heart Disease"]

                        st.write("### Prediction Results")
                        st.dataframe(data[['age', 'sex', 'chol', 'trestbps', 'thalach', 'Prediction']])

                        # Visualize prediction results
                        st.write("### Prediction Overview")
                        prediction_counts = data['Prediction'].value_counts().reset_index()
                        prediction_counts.columns = ['Prediction', 'Count']
                        fig = px.bar(prediction_counts, x='Prediction', y='Count', color='Prediction', 
                                     title="Heart Disease Prediction Results", 
                                     color_discrete_sequence=['green', 'red'])
                        st.plotly_chart(fig)

                        # Display advice for diseased individuals
                        if not diseased.empty:
                            st.subheader("⚠️ Advice for Individuals with Heart Disease")
                            st.markdown(
                                """
                                - **Seek medical advice** immediately.
                                - **Follow a heart-healthy lifestyle**: balanced diet, regular exercise, and stress management.
                                - **Stay on prescribed medications** and have regular check-ups.
                                """
                            )
                            st.write("### Affected Individuals")
                            st.dataframe(diseased[['age', 'sex', 'chol', 'trestbps', 'thalach', 'Prediction']])

                        # Display tips for unaffected individuals
                        if not undiseased.empty:
                            st.subheader("✅ Tips for Maintaining Heart Health")
                            st.markdown(
                                """
                                - **Eat a nutritious diet** rich in fruits, vegetables, and whole grains.
                                - **Stay physically active**.
                                - **Avoid smoking** and manage stress.
                                - **Monitor your health** regularly.
                                """
                            )
                            st.write("### Unaffected Individuals")
                            st.dataframe(undiseased[['age', 'sex', 'chol', 'trestbps', 'thalach', 'Prediction']])
                    except Exception as e:
                        st.error(f"Error during prediction: {e}")
            else:
                st.warning(f"Missing required columns: {', '.join([col for col in required_columns if col not in data.columns])}")
        except Exception as e:
            st.error(f"Error processing the file: {e}")
    else:
        if uploaded_file is None:
            st.info("Please upload a CSV or Excel file.")
        if heart_disease_model is None:
            st.error("Model not loaded. Verify the model path.")

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
