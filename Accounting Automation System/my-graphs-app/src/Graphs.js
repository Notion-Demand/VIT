// src/Graphs.js
import React from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, LineElement, CategoryScale, LinearScale } from 'chart.js';

// Register the required components with Chart.js
ChartJS.register(LineElement, CategoryScale, LinearScale);

// Sample data for graphs (replace with actual data)
const data = {
  labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'], // X-axis labels
  datasets: [
    {
      label: 'Sample Data',
      data: [10, 20, 15, 25, 30], // Y-axis data
      borderColor: 'rgba(75,192,192,1)',
      backgroundColor: 'rgba(75,192,192,0.2)',
    },
  ],
};

const Graphs = () => {
  return (
    <div>
      <h2>Risk Management Graph</h2>
      <Line data={data} />

      <h2>Portfolio Optimization Graph</h2>
      <Line data={data} />

      <h2>Regulatory Compliance Graph</h2>
      <Line data={data} />

      <h2>Customer Insights Graph</h2>
      <Line data={data} />

      <h2>Operational Efficiency Graph</h2>
      <Line data={data} />
    </div>
  );
};

export default Graphs;
