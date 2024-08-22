from flask import Flask, request, jsonify, render_template, redirect, url_for
import os
from PyPDF2 import PdfReader
import re
import json

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

REFERENCE_RANGES = {
    'Hemoglobin': (13.00, 17.00),
    'Packed Cell Volume (PCV)': (40.00, 50.00),
    'RBC Count': (4.50, 5.50),
    'MCV': (83.00, 101.00),
    'MCH': (27.00, 32.00),
    'MCHC': (31.50, 34.50),
    'Red Cell Distribution Width (RDW)': (11.60, 14.00),
    'Total Leukocyte Count (TLC)': (4.00, 10.00),
    'Segmented Neutrophils': (40.00, 80.00),
    'Lymphocytes': (20.00, 40.00),
    'Monocytes': (2.00, 10.00),
    'Eosinophils': (1.00, 6.00),
    'Basophils': (0.00, 2.00),
    'Platelet Count': (150.00, 410.00),
    'Mean Platelet Volume': (6.5, 12.0)
}

# Load precautions from a JSON file
with open('precautions.json') as f:
    PRECAUTIONS = json.load(f)

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

def parse_blood_report(text):
    results = {}
    name_match = re.search(r'Name\s*(?::|)\s*(\w+)', text)
    patient_name = name_match.group(1) if name_match else "Unknown"
    
    for test_name, ref_range in REFERENCE_RANGES.items():
        pattern = f"{test_name}.*?([0-9.]+)"
        match = re.search(pattern, text, re.DOTALL)
        if match:
            value = float(match.group(1))
            results[test_name] = (value, ref_range)
    return patient_name, results

def analyze_report(results):
    analysis = {}
    precautions = {}
    all_good = True
    
    for test_name, (value, (low, high)) in results.items():
        status = "Normal"
        if value < low:
            status = "Critical"
            precautions[test_name] = PRECAUTIONS.get(test_name, "Consult your doctor.")
            all_good = False
        elif value > high:
            status = "Critical"
            precautions[test_name] = PRECAUTIONS.get(test_name, "Consult your doctor.")
            all_good = False
        elif low < value < high * 0.9:
            status = "Warning"
            precautions[test_name] = PRECAUTIONS.get(test_name, "Consult your doctor.")
            all_good = False
        analysis[test_name] = (value, (low, high), status)
    
    if all_good:
        return analysis, "All Good", {}
    else:
        return analysis, "Precautions needed", precautions

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            pdf_text = extract_text_from_pdf(file_path)
            patient_name, report_results = parse_blood_report(pdf_text)
            analysis, summary, precautions = analyze_report(report_results)
            return render_template('index.html', patient_name=patient_name, analysis=analysis, summary=summary, precautions=precautions)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
