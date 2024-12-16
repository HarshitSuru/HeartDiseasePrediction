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
        The Health Assistant leverages a machine learning model to evaluate the likelihood of heart disease 
        based on health indicators such as age, cholesterol levels, blood pressure, and more. 
        It provides preliminary insights for individuals and healthcare professionals.

        ### 🔉 Note
        Please note that this tool is intended for informational purposes only and does not replace 
        professional medical advice. Always consult a qualified healthcare provider for accurate diagnosis and treatment.
        """
    )

# Heart Disease Prediction page
if selected == "Heart Disease Prediction":
    st.title("🩺 Heart Disease Prediction System")
    st.markdown(
        """
        Upload patient health data to predict the likelihood of heart disease and receive tailored advice.

        ### 📖 How to Use
        1. Navigate to the **Heart Disease Prediction** section using the sidebar.
        2. Upload a CSV or Excel file containing the required health information for each patient.
        3. Click on the **Predict Heart Disease** button to generate predictions.
        4. View the results and get actionable advice for affected individuals.
        """
    )

    # File upload
    st.subheader("📂 Upload Patient Data")
    uploaded_file = st.file_uploader("Upload a CSV/Excel file with patient data:", type=["csv", "xlsx"])

    # Load model
    heart_disease_model = None
    model_path = r'C:\Users\suruh\OneDrive\Desktop\HeartDiseasePrediction\Heart-Disease-Prediction\saved_models\heart_disease_model.sav'

    try:
        if os.path.exists(model_path):
            heart_disease_model = pickle.load(open(model_path, 'rb'))
            st.success("Model successfully loaded! Please proceed with uploading data for prediction.")
        else:
            st.error(f"Model file not found at: {model_path}")
    except Exception as e:
        st.error(f"Error loading model: {e}")

    # Proceed if file is uploaded and model is loaded
    if uploaded_file is not None and heart_disease_model is not None:
        # Read file
        try:
            if uploaded_file.type == "text/csv":
                data = pd.read_csv(uploaded_file)
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                data = pd.read_excel(uploaded_file)

            st.write("### Data Preview")
            st.dataframe(data.head())

            # Visualize distributions of key features
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

                        if not diseased.empty:
                            st.subheader("⚠️ Advice for Individuals with Heart Disease")
                            st.markdown(
                                """
                                - **Seek immediate medical consultation.**
                                - **Adopt a heart-healthy lifestyle**: balanced diet, regular exercise, and stress management.
                                - **Follow prescribed treatments** and attend regular medical check-ups.
                                """
                            )
                            st.write("### Affected Individuals")
                            st.dataframe(diseased[['age', 'sex', 'chol', 'trestbps', 'thalach', 'Prediction']])

                            # Visualize demographic insights for diseased patients
                            if 'sex' in diseased.columns:
                                sex_distribution = diseased['sex'].value_counts().reset_index()
                                sex_distribution.columns = ['Sex', 'Count']
                                fig = px.bar(sex_distribution, x='Sex', y='Count', title="Gender Distribution (Affected)", 
                                             color='Sex', color_discrete_sequence=['blue', 'pink'])
                                st.plotly_chart(fig)

                        if not undiseased.empty:
                            st.subheader("✅ Tips for Maintaining Heart Health")
                            st.markdown(
                                """
                                - **Eat a nutritious diet** rich in fruits, vegetables, and whole grains.
                                - **Stay physically active** with regular exercise.
                                - **Avoid smoking** and manage stress effectively.
                                - **Monitor your health regularly.**
                                """
                            )
                            st.write("### Unaffected Individuals")
                            st.dataframe(undiseased[['age', 'sex', 'chol', 'trestbps', 'thalach', 'Prediction']])
                    except Exception as e:
                        st.error(f"Prediction error: {e}")
            else:
                st.warning(f"Missing required columns: {', '.join([col for col in required_columns if col not in data.columns])}")
        except Exception as e:
            st.error(f"File processing error: {e}")
    else:
        if uploaded_file is None:
            st.info("Please upload a valid CSV or Excel file.")
        if heart_disease_model is None:
            st.error("Model not loaded. Verify the model file path.")

# About Us page
if selected == "About Us":
    st.title("👨‍💼 About Us")
    st.markdown(
        """
        ### Dedicated to leveraging technology for health risk prediction and management.

        #### Connect with the Developer
        - [GitHub](https://github.com/HarshitSuru/)
        - [LinkedIn](https://www.linkedin.com/in/suru-harshit-4863372bb)
        - Email: [suruharshit2005@gmail.com](mailto:suruharshit2005@gmail.com)
        """
    )
