# Heart Disease Prediction Streamlit App

This repository contains the codebase for the **Heart Disease Prediction Streamlit App**. The app allows users to predict the likelihood of certain diseases based on input parameters.

## Project Overview
The primary goal of this app is to provide a user-friendly interface for predicting diseases. The project includes:
- **Streamlit App**: `app.py` - The main file for running the Streamlit app.
- **Training Notebooks**: Contains Jupyter notebooks used to train models.
- **Datasets**: The datasets used for training the models are provided in the `datasets` folder.

## Model and Accuracy
For heart disease prediction, we used Logistic Regression, achieving an accuracy of **85%** on the test data.

## Installation
To set up the project, follow these steps:

1. Clone this repository:
    ```bash
    git clone https://github.com/your-username/Multiple-Disease-Prediction-App.git
    ```

2. Navigate to the project directory:
    ```bash
    cd Multiple-Disease-Prediction-App
    ```

3. Install the required dependencies for the Streamlit app:
    ```bash
    pip install -r requirements.txt
    ```

4. Additional libraries may be needed to run the Jupyter notebooks. Install them as needed.

## Running the App
To start the Streamlit app, use the following command:
```bash
streamlit run app.py
