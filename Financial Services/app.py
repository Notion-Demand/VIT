from flask import Flask, request, jsonify, send_file
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import os
import traceback
from flask_cors import CORS
from flask import after_this_request
from sklearn.model_selection import RandomizedSearchCV

app = Flask(__name__)
CORS(app)

# Route for fraud detection
@app.route('/fraud-detection', methods=['POST'])
def fraud_detection():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(file)
    dfc = df.copy()

    # Handle missing values using SimpleImputer
    imputer = SimpleImputer(strategy='mean')
    df[df.select_dtypes(include=['float64', 'int64']).columns] = imputer.fit_transform(
        df.select_dtypes(include=['float64', 'int64'])
    )

    # Identify categorical columns and apply label encoding
    categorical_columns = df.select_dtypes(include=['object']).columns
    for col in categorical_columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))

    # Standardize numerical features
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    scaler = StandardScaler()
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    # Isolation Forest for anomaly detection
    model = IsolationForest(n_estimators=400, contamination=0.06, random_state=42, max_samples='auto')

    # Fit the model and make predictions
    model.fit(df)

    # Convert DataFrame to NumPy array for decision_function
    df_values = df.values
    df['anomaly_score'] = model.decision_function(df_values)

    df['predicted_fraud'] = model.fit_predict(df_values)

    # Map predictions to 1 for fraud (-1 from the model) and 0 for non-fraud (1 from the model)
    df['predicted_fraud'] = df['predicted_fraud'].map({1: 0, -1: 1})

    # Normalize the decision function values to represent probabilities (0 to 1)
    df['fraud_probability'] = (df['anomaly_score'] - df['anomaly_score'].min()) / (
            df['anomaly_score'].max() - df['anomaly_score'].min())

    dfc['predicted_fraud'] = df['predicted_fraud']
    dfc['fraud_probability'] = df['fraud_probability']

    # Get the count of fraud cases detected
    fraud_count = dfc['predicted_fraud'].sum()

    # If 'FraudFound_P' is present, calculate evaluation metrics
    if 'FraudFound_P' in dfc.columns:
        actual = dfc['FraudFound_P'].values
        predicted = dfc['predicted_fraud'].values
        try:
            accuracy = accuracy_score(actual, predicted)
            precision = precision_score(actual, predicted)
            recall = recall_score(actual, predicted)
            f1 = f1_score(actual, predicted)
            roc_auc = roc_auc_score(actual, predicted)
        except ValueError as e:
            return jsonify({'error': f'Error calculating metrics: {e}'}), 500
    else:
        accuracy = precision = recall = f1 = roc_auc = None

    # Save the result to a CSV file
    result_filename = 'fraud_detection_result.csv'
    dfc.to_csv(result_filename, index=False)

    return jsonify({
        'fraud_count': int(fraud_count),
        'metrics': {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'roc_auc': roc_auc
        },
        'preview': dfc.head(10).to_dict(orient='records'),
        'result_file': result_filename
    })

# Route for downloading the result file
@app.route('/download', methods=['GET'])
def download_file():
    file_path = 'fraud_detection_result.csv'

    if os.path.exists(file_path):
        @after_this_request
        def remove_file(response):
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error deleting file: {e}")
            return response

        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({"error": "File not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
