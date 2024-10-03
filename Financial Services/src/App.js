import React, { useState } from 'react';
import './App.css';
import axios from 'axios';

function App() {
  const [file, setFile] = useState(null);
  const [targetColumn, setTargetColumn] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [dataRows, setDataRows] = useState([]);
  const [error, setError] = useState('');

  // Handle file input
  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  // Handle form submission
  const handleSubmit = async (event) => {
    event.preventDefault();
    setError(''); // Reset error state

    if (!file || !targetColumn) {
      setError("Please upload a file and specify the target column.");
      return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('target_column', targetColumn);

    setLoading(true);

    try {
      const response = await axios.post('http://localhost:5000/fraud-detection', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (response.data) {
        setResults(response.data);
        alert(`Fraud count detected: ${response.data.fraud_count}`);
        setDataRows(response.data.preview_data);
      } else {
        console.error("No data returned from the server");
      }
    } catch (error) {
      console.error("There was an error with the request:", error.response?.data || error.message);
      setError("Error: " + (error.response?.data?.error || error.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <h1>Fraud Detection</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Upload Dataset (CSV):</label>
          <input type="file" accept=".csv" onChange={handleFileChange} />
        </div>
        <div>
          <label>Target Column:</label>
          <input
            type="text"
            value={targetColumn}
            onChange={(e) => setTargetColumn(e.target.value)}
            placeholder="Enter target column name"
          />
        </div>
        {error && <p style={{ color: 'red' }}>{error}</p>} {/* Display error message */}
        <div>
          <button type="submit" disabled={loading}>
            {loading ? "Processing..." : "Submit"}
          </button>
        </div>
      </form>

      {results && (
        <div className="results">
          <h2>Results:</h2>
          <p><strong>Accuracy: </strong>{results.accuracy}</p>
          <p><strong>Precision: </strong>{results.precision}</p>
          <p><strong>F1 Score: </strong>{results.f1_score}</p>
          <p><strong>ROC AUC Score: </strong>{results.roc_auc_score}</p>
          <p><strong>Fraud Count: </strong>{results.fraud_count}</p>
          
          <h3>Preview of First 30 Rows:</h3>
          {dataRows.length > 0 && (
            <table>
              <thead>
                <tr>
                  {Object.keys(dataRows[0]).map((key) => (
                    <th key={key}>{key}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
  {dataRows.map((row, index) => (
    <tr key={index} className={row.Fraud_Detected ? 'fraud-row' : ''}>
      {Object.values(row).map((value, i) => (
        <td key={i}>{value}</td>
      ))}
    </tr>
  ))}
</tbody>

            </table>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
