from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, f1_score, roc_auc_score
from imblearn.over_sampling import SMOTE
import traceback
import numpy as np


app = Flask(__name__)
CORS(app)

@app.route('/fraud-detection', methods=['POST'])
def fraud_detection():
    if 'file' not in request.files or 'target_column' not in request.form:
        return jsonify({"error": "File or target column missing"}), 400

    file = request.files['file']
    target_column = request.form['target_column']
    
    try:
        # Load the dataset
        df = pd.read_csv(file)
        
        # Ensure the target column exists in the DataFrame
        if target_column not in df.columns:
            return jsonify({'error': f'Target column "{target_column}" not found in the dataset'}), 400

        # Preprocess
        X = df.drop(target_column, axis=1)
        y = df[target_column]
        
        # Identify categorical columns
        categorical_columns = X.select_dtypes(include=['object']).columns
        
        # Apply label encoding to categorical columns
        for col in categorical_columns:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
        
        # Feature Scaling
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Handle imbalanced classes
        smote = SMOTE(random_state=42)
        X_resampled, y_resampled = smote.fit_resample(X_scaled, y)

        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

        # Hyperparameter tuning with RandomizedSearchCV
        param_dist = {
            'n_estimators': [100, 200, 300],
            'max_features': ['sqrt', 'log2'],
            'max_depth': [None, 10, 20, 30, 40],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4],
            'bootstrap': [True, False],
            'class_weight': ['balanced', None]
        }
        
        model = RandomForestClassifier(random_state=42)
        random_search = RandomizedSearchCV(estimator=model, param_distributions=param_dist,
                                           n_iter=100, cv=5, verbose=2, random_state=42, n_jobs=2)
        random_search.fit(X_train, y_train)

        # Best model
        best_model = random_search.best_estimator_

        # Predict
        y_pred = best_model.predict(X_test)
        y_pred_proba = best_model.predict_proba(X_test)[:, 1]

        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='binary')
        f1 = f1_score(y_test, y_pred, average='binary')
        roc_auc = roc_auc_score(y_test, y_pred_proba)

        # Add predictions to the original dataframe
        df['Fraud_Detected'] = best_model.predict(scaler.transform(X))

        # Count of frauds detected
        fraud_count = df['Fraud_Detected'].sum()

        # Get first 30 rows
        preview_data = df.head(30).to_dict(orient='records')

        # Convert all values to standard Python types
        response = {
            "accuracy": accuracy,
            "precision": precision,
            "f1_score": f1,
            "roc_auc_score": roc_auc,
            "fraud_count": fraud_count,
            "preview_data": preview_data
        }

        # Convert numpy types to standard Python types for JSON serialization
        for key in response:
            if isinstance(response[key], (np.int64, np.float64)):
                response[key] = float(response[key]) if isinstance(response[key], np.float64) else int(response[key])
        
        return jsonify(response)
    
    except Exception as e:
        print(traceback.format_exc())  # Print stack trace to console
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
