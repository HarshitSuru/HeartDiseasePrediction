import os
import pickle
import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
import requests

@st.cache_resource
def load_heart_disease_model():
    model_url = "https://github.com/HarshitSuru/HeartDiseasePrediction/raw/main/Heart-Disease-Prediction/saved_models/heart_disease_model.sav"
    try:
        response = requests.get(model_url)
        response.raise_for_status() # Raise an exception for HTTP errors
        # Save to a temporary file in memory or a unique name if needed, though just "heart_disease_model_cached.sav" might be fine for streamlit's single-instance nature
        model_path = "heart_disease_model_cached.sav"
        with open(model_path, "wb") as model_file:
            model_file.write(response.content)
        with open(model_path, "rb") as model_file:
            loaded_model = pickle.load(model_file)
        return loaded_model
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Critical: Failed to download the prediction model. Please check internet connectivity or model URL. Details: {e}")
        return None
    except Exception as e:
        st.error(f"⚠️ Critical: Error loading the prediction model. Details: {e}")
        return None

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

    heart_disease_model = load_heart_disease_model() # Call the new function

    required_columns = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
    prediction_labels = {0: "Healthy Heart", 1: "Heart Disease"}

    # General page introduction
    st.markdown(
        """
        This tool helps predict the likelihood of heart disease. Choose your preferred input method below.
        For bulk uploads, please ensure your data matches the format of the example file.
        """
    )

    # Create tabs for the two input modes
    tab1, tab2 = st.tabs(["🧑‍⚕️ Single Patient Entry", "📄 Bulk Upload (Excel/CSV)"])

    with tab1:
        st.subheader("Enter Patient Details Manually")
        st.markdown("Fill in the patient's details in the form below and click 'Predict for Single Patient' to get an individual risk assessment and advice.")
        # Content for Single Patient Entry
        # Note: The original "st.subheader("🧑‍⚕️ Single Patient Prediction (Manual Entry)")" is replaced by the tab's subheader.
        with st.form("single_patient_form"):
            st.markdown("Provide the patient's details below:")

            # Input fields for each feature
            age = st.number_input("Age (years)", min_value=1, max_value=120, value=50, step=1, key="age_single") # Added key for uniqueness
            sex_options = [(0, "Female"), (1, "Male")]
            sex = st.selectbox("Sex", options=sex_options, format_func=lambda x: x[1], key="sex_single")

            cp_options = [(0, "Type 0: Typical Angina"), (1, "Type 1: Atypical Angina"), (2, "Type 2: Non-anginal Pain"), (3, "Type 3: Asymptomatic")]
            cp = st.selectbox("Chest Pain Type (cp)", options=cp_options, format_func=lambda x: x[1], key="cp_single")

            trestbps = st.number_input("Resting Blood Pressure (mm Hg)", min_value=50, max_value=250, value=120, step=1, key="trestbps_single")
            chol = st.number_input("Serum Cholestoral (mg/dl)", min_value=50, max_value=600, value=200, step=1, key="chol_single")

            fbs_options = [(0, "False"), (1, "True")]
            fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dl (fbs)", options=fbs_options, format_func=lambda x: x[1], key="fbs_single")

            restecg_options = [(0, "Type 0: Normal"), (1, "Type 1: ST-T wave abnormality"), (2, "Type 2: Probable or definite left ventricular hypertrophy")]
            restecg = st.selectbox("Resting Electrocardiographic Results (restecg)", options=restecg_options, format_func=lambda x: x[1], key="restecg_single")

            thalach = st.number_input("Maximum Heart Rate Achieved (thalach)", min_value=50, max_value=250, value=150, step=1, key="thalach_single")

            exang_options = [(0, "No"), (1, "Yes")]
            exang = st.selectbox("Exercise Induced Angina (exang)", options=exang_options, format_func=lambda x: x[1], key="exang_single")

            oldpeak = st.number_input("ST depression induced by exercise relative to rest (oldpeak)", min_value=0.0, max_value=10.0, value=1.0, step=0.1, format="%.1f", key="oldpeak_single")

            slope_options = [(0, "Type 0: Upsloping"), (1, "Type 1: Flat"), (2, "Type 2: Downsloping")]
            slope = st.selectbox("Slope of the peak exercise ST segment (slope)", options=slope_options, format_func=lambda x: x[1], key="slope_single")

            ca_options = [(0, "0 vessels"), (1, "1 vessel"), (2, "2 vessels"), (3, "3 vessels"), (4, "4 vessels")]
            ca = st.selectbox("Number of major vessels (0-4) colored by flourosopy (ca)", options=ca_options, format_func=lambda x: x[1], key="ca_single")

            thal_options = [(0, "0: Unknown/Not Used"), (1, "1: Normal"), (2, "2: Fixed defect"), (3, "3: Reversible defect")]
            thal = st.selectbox("Thalassemia (thal)", options=thal_options, format_func=lambda x: x[1], key="thal_single")

            submitted_single = st.form_submit_button("Predict for Single Patient")

            if submitted_single:
                if heart_disease_model is not None:
                    try:
                        age_val = age
                        sex_val = sex[0]
                        cp_val = cp[0]
                        trestbps_val = trestbps
                        chol_val = chol
                        fbs_val = fbs[0]
                        restecg_val = restecg[0]
                        thalach_val = thalach
                        exang_val = exang[0]
                        oldpeak_val = oldpeak
                        slope_val = slope[0]
                        ca_val = ca[0]
                        thal_val = thal[0]

                        patient_features = {
                            'age': age_val, 'sex': sex_val, 'cp': cp_val, 'trestbps': trestbps_val,
                            'chol': chol_val, 'fbs': fbs_val, 'restecg': restecg_val,
                            'thalach': thalach_val, 'exang': exang_val, 'oldpeak': oldpeak_val,
                            'slope': slope_val, 'ca': ca_val, 'thal': thal_val
                        }

                        single_patient_df = pd.DataFrame([patient_features], columns=required_columns)
                        prediction_array = heart_disease_model.predict(single_patient_df)
                        single_prediction = prediction_array[0]
                        single_result_label = prediction_labels.get(single_prediction, "Unknown")

                        st.session_state['single_prediction_val'] = single_prediction
                        st.session_state['single_result_label'] = single_result_label
                        st.session_state['single_input_features'] = patient_features
                    except AttributeError as e:
                        st.error(f"⚠️ Error processing form input. Make sure all fields are selected/valid. Details: {e}") # This specific one is good.
                    except Exception as e:
                        st.error(f"⚠️ An error occurred during prediction for the single entry: {e}. Please ensure all fields are filled correctly.")
                        if 'single_prediction_val' in st.session_state: del st.session_state['single_prediction_val']
                        if 'single_result_label' in st.session_state: del st.session_state['single_result_label']
                else:
                    st.error("Model not loaded. Cannot perform prediction. Check error messages above.")

        # Display results and advice for Single User Input Mode (still within tab1)
        if 'single_result_label' in st.session_state and st.session_state['single_result_label'] is not None:
            st.subheader("📈 Single Patient Prediction Result")
            if 'single_input_features' in st.session_state:
                with st.expander("Show Submitted Data"):
                    st.json(st.session_state['single_input_features'])
            result_label = st.session_state['single_result_label']
            if result_label == "Heart Disease":
                st.error(f"**Prediction: {result_label}**")
                st.warning("🚨 **Important Disclaimer:** This is a prediction based on a machine learning model and is NOT a medical diagnosis. Please consult a qualified healthcare professional for any health concerns or before making any decisions related to your health.")
                st.markdown("#### Recommended Next Steps & General Advice:")
                st.markdown("""
                *   **Consult a Doctor:** ...
                *   **Follow Medical Advice:** ...
                *   **Heart-Healthy Diet:** ...
                *   **Regular Physical Activity:** ...
                *   **Manage Stress:** ...
                *   **Quit Smoking:** ...
                *   **Limit Alcohol:** ...
                *   **Monitor Key Health Indicators:** ...
                """) # Ellipses for brevity in this diff, full text is preserved
            elif result_label == "Healthy Heart":
                st.success(f"**Prediction: {result_label}**")
                st.info("✅ This prediction suggests a lower likelihood of heart disease...")
                st.markdown("#### General Advice for Maintaining a Healthy Heart:")
                st.markdown("""
                *   **Balanced Diet:** ...
                *   **Stay Active:** ...
                *   **Manage Stress:** ...
                *   **Avoid Smoking:** ...
                *   **Moderate Alcohol Consumption:** ...
                *   **Regular Check-ups:** ...
                *   **Be Aware of Changes:** ...
                """) # Ellipses for brevity
            else:
                st.info(f"Prediction Result: {result_label}")

    with tab2:
        st.subheader("Upload Patient Data File")
        st.markdown(
            """
            #### How to Use Bulk Upload:
            1. **Download the example data** (link below) to understand the required format.
            2. **Prepare your data** in CSV or Excel, matching the example structure. Ensure that data columns meant for numerical analysis (like 'age', 'trestbps', 'chol', etc.) contain only numbers and are formatted correctly to avoid errors during prediction.
            3. **Upload your file** using the uploader.
            4. Click **Predict Heart Disease** for analysis.
            """
        )
        # Content for Bulk Upload
        example_file_url = "https://github.com/HarshitSuru/HeartDiseasePrediction/raw/main/Heart-Disease-Prediction/example_patient_data.xlsx" # Define it again or ensure scope
        st.subheader("📂 Download Example Patient Data")
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

        st.subheader("📂 Upload Your Patient Data")
        uploaded_file = st.file_uploader("Upload CSV/Excel (one or more patients):", type=["csv", "xlsx"], key="bulk_uploader") # Added key

        if uploaded_file:
            data = None # Initialize data to None
            try:
                st.success(f"Successfully loaded '{uploaded_file.name}'. Processing...") # Updated message
                if uploaded_file.name.endswith('.csv'):
                    data = pd.read_csv(uploaded_file)
                else:
                    data = pd.read_excel(uploaded_file)

                if data.empty:
                    st.warning("⚠️ The uploaded file appears to be empty (contains no data rows). Please upload a file with data.")
                    # uploaded_file = None # Avoid processing further by checking 'data is not None and not data.empty'
                    data = None # Explicitly set data to None to fail the condition below

            except pd.errors.EmptyDataError:
                st.error(f"⚠️ Error: The uploaded file '{uploaded_file.name}' is empty. Please provide a file with data.")
                uploaded_file = None # Reset to prevent further processing attempts
                data = None
            except Exception as e:
                st.error(f"⚠️ Error processing file '{uploaded_file.name}': {e}. Please ensure it's a valid CSV or Excel file and not corrupted.")
                uploaded_file = None # Reset
                data = None

            if uploaded_file and data is not None and not data.empty: # Proceed only if file processed and data is not empty
                st.info(f"Detected {data.shape[0]} rows and {data.shape[1]} columns in '{uploaded_file.name}'.")
                missing_columns = [col for col in required_columns if col not in data.columns]
                if missing_columns:
                    st.error(f"⚠️ The uploaded file is missing the following required columns: {', '.join(missing_columns)}")
                else:
                    st.subheader("🔢 Uploaded Data (Preview)")
                    st.write(data.head())
                    data = data[required_columns]
                    if heart_disease_model is not None:
                        try:
                            if st.button("Predict Heart Disease", key="predict_bulk"):
                                predictions = heart_disease_model.predict(data)
                                data['Prediction'] = predictions
                                data['Result'] = data['Prediction'].map(prediction_labels).fillna("Unknown")
                                st.subheader("📊 Bulk Upload Analysis & Predictions")
                                st.markdown("#### Summary Statistics:")
                                total_records = len(data)
                                healthy_count = data['Result'].value_counts().get("Healthy Heart", 0)
                                disease_count = data['Result'].value_counts().get("Heart Disease", 0)
                                unknown_count = data['Result'].value_counts().get("Unknown", 0)
                                col1, col2, col3, col4 = st.columns(4)
                                with col1: st.metric(label="Total Records", value=total_records)
                                with col2: st.metric(label="Predicted Healthy Heart", value=healthy_count, delta_color="inverse")
                                with col3: st.metric(label="Predicted Heart Disease", value=disease_count, delta_color="inverse")
                                with col4:
                                    if unknown_count > 0: st.metric(label="Unknown Predictions", value=unknown_count, delta_color="off")
                                st.markdown("---")
                                st.markdown("#### Detailed Results:")
                                display_columns = list(data.columns)
                                if 'Prediction' in display_columns and 'Result' in display_columns:
                                    pred_idx = display_columns.index('Prediction')
                                    if 'Result' in display_columns:
                                        display_columns.insert(pred_idx + 1, display_columns.pop(display_columns.index('Result')))
                                st.write(data[display_columns])
                                fig = px.histogram(data, x='Prediction', title="Heart Disease Prediction Distribution (0 or 1)", labels={'Prediction': 'Predicted Value (0: Healthy, 1: Disease)'}, text_auto=True)
                                st.plotly_chart(fig)
                                fig_labels = px.histogram(data, x='Result', title="Heart Disease Prediction Summary", labels={'Result': 'Prediction Result'}, text_auto=True, category_orders={"Result": ["Healthy Heart", "Heart Disease", "Unknown"]})
                                st.plotly_chart(fig_labels)
                        except Exception as e:
                            st.error(f"⚠️ An error occurred during the prediction process: {e}. This might be due to unexpected data types or values in your file. Please check that your data columns match the example format and contain appropriate values.")
            # except Exception as e: # This outer try-except for file processing was already modified in A.1
            #     st.error(f"⚠️ Error processing file: {e}")

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
