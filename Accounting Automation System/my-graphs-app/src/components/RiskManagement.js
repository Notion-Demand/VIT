import React, { useState, useEffect } from 'react';
import Papa from 'papaparse';
import { Line } from 'react-chartjs-2';
import 'chart.js/auto';

const RiskManagement = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    // Load and parse CSV file
    Papa.parse('..my-graphs-app\public\RBIB.csv', {
      download: true,
      header: true,
      complete: (results) => {
        const { data } = results;
        const time = data.map(row => row['Time']);
        const marketRisk = data.map(row => parseFloat(row['Market Risk']) || 0);
        const creditRisk = data.map(row => parseFloat(row['Credit Risk']) || 0);
        const operationalRisk = data.map(row => parseFloat(row['Operational Risk']) || 0);

        setData({
          labels: time,
          datasets: [
            {
              label: 'Market Risk',
              data: marketRisk,
              fill: false,
              borderColor: 'rgba(75,192,192,1)',
            },
            {
              label: 'Credit Risk',
              data: creditRisk,
              fill: false,
              borderColor: 'rgba(153,102,255,1)',
            },
            {
              label: 'Operational Risk',
              data: operationalRisk,
              fill: false,
              borderColor: 'rgba(255,159,64,1)',
            },
          ],
        });
      },
    });
  }, []);

  const options = {
    scales: {
      x: {
        title: {
          display: true,
          text: 'Time',
        },
      },
      y: {
        title: {
          display: true,
          text: 'Risk Level',
        },
      },
    },
  };

  return (
    <div>
      <h2>Risk Management: Forecast of Different Risks</h2>
      {data ? <Line data={data} options={options} /> : <p>Loading data...</p>}
    </div>
  );
};

export default RiskManagement;
