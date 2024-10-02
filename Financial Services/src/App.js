import React, { useState } from 'react';
import './App.css';
import axios from 'axios';

function App() {
  const [file, setFile] = useState(null);
  const [targetColumn, setTargetColumn] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [data, setData] = useState([]);

  // Handle file input
  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  // Handle form submission
  const handleSubmit = async (event) => {
    event.preventDefault();
    
    if (!file || !targetColumn) {
      alert("Please upload a file and specify the target column.");
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

      setResults(response.data);
      setData(response.data.data); // Set the dataset for rendering

    } catch (error) {
      console.error("There was an error with the request:", error);
    }

    setLoading(false);
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
        <div>
          <button type="submit" disabled={loading}>
            {loading ? "Processing..." : "Submit"}
          </button>
        </div>
      </form>

      {results && (
        <div className="results">
          <h2>Results:</h2>
          <p><strong>Accuracy: </strong> {results.accuracy}</p>
          <p><strong>Precision: </strong>{results.precision}</p>
          <p><strong>F1 Score: </strong>{results.f1_score}</p>
          <p><strong>ROC AUC Score: </strong>{results.roc_auc_score}</p>

          <h3>Top 30 Rows:</h3>
          <table className="data-table">
            <thead>
              <tr>
                {data.length > 0 && Object.keys(data[0]).map((key) => (
                  <th key={key}>{key}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {data.map((row, index) => (
                <tr key={index} style={{ backgroundColor: row.Predicted_Fraud === 1 ? 'red' : 'white' }}>
                  {Object.values(row).map((val, i) => (
                    <td key={i}>{val}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default App;
