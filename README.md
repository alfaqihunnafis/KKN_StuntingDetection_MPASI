# Stunting Detection Web
## Overview
Stunting Prediction Web is a web application developed using Flask that predicts whether a child is experiencing stunting based on various input features. This application provides two modes:

1. Individual Prediction: Allows the user to input individual data for prediction.
2. Group Prediction: Allows the user to upload a CSV file containing multiple records for batch prediction.

The underlying model used is Random Forest, which was trained using data related to child growth.

## Features
1. Predict stunting for a single individual.
2. Upload a CSV file to predict stunting for multiple individuals.
3. Download the results of group predictions in a CSV file.

## Tech Stack
1. Backend: Flask (Python)
2. Frontend: HTML & CSS
3. Machine Learning: Random Forest (scikit-learn)
4. Data Handling: Pandas, Numpy

## Instalation and Setup
1. Clone the repository

To get started, clone this repository to your local machine:
```bash
git clone https://github.com/silviansi/stunting-detection-web
cd stunting-detection-web
```
2. Install Dependencies

Ensure you have Python installed. Install the required Python packages using `pip`
```bash
pip install -r requirements.txt
```
The `requirements.txt` file includes dependencies like Flask, Pandas, NumPy, and scikit-learn.

3. Model Setup
Make sure you have the pre-trained Random Forest model file (`modelRF.pkl`) in the `model/` directory. If you don’t have the model file, you will need to train one and save it as `modelRF.pkl` in the appropriate directory.

4. Running the Application
To start the Flask application, run the following command in the project directory:
```bash
python app.py
```
By default, the application will run on `http://127.0.0.1:5000/`. Open a browser and navigate to this address to start using the web interface.

5. Uploading CSV for Group Prediction
Ensure that your CSV file follows the correct format with columns:

- Jenis Kelamin (0 for female, 1 for male)
- Umur (bulan)
- Berat Bayi (kg)
- Panjang Bayi (cm)
- Berat Badan (kg)
- Tinggi Badan (cm)
Once uploaded, the application will predict stunting status for each individual and provide an option to download the result as a CSV file.
## Example
```bash
Jenis Kelamin,Umur (bulan),Berat Bayi (kg),Panjang Bayi (cm),Berat Badan (kg),Tinggi Badan (cm)
1,12,3.5,50,10.2,75
0,24,4.0,55,11.3,80
```
## Troubleshooting
- Ensure that the correct format is used for the CSV file during group predictions.
- If you encounter errors related to model loading, verify that the `modelRF.pkl` file exists in the `model/` directory.
