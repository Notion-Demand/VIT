import React from 'react';
import { Line, Bar, Scatter } from 'react-chartjs-2';
import 'chart.js/auto';

const OtherGraphs = () => {
  // Data and options for the different graphs
  const demandData = {
    labels: Array.from({ length: 120 }, (_, i) => i),
    datasets: [
      {
        label: 'Historical Demand',
        data: Array.from({ length: 100 }, () => Math.random() * 10 + 100),
        borderColor: 'blue',
        fill: false,
      },
      {
        label: 'Forecasted Demand',
        data: Array.from({ length: 20 }, () => Math.random() * 5 + 100),
        borderColor: 'orange',
        borderDash: [5, 5],
        fill: false,
      },
    ],
  };

  const cashFlowData = {
    labels: Array.from({ length: 120 }, (_, i) => i),
    datasets: [
      {
        label: 'Historical Cash Flow',
        data: Array.from({ length: 100 }, () => Math.random() * 1000 + 5000),
        borderColor: 'green',
        fill: false,
      },
      {
        label: 'Forecasted Cash Flow',
        data: Array.from({ length: 20 }, () => Math.random() * 500 + 5000),
        borderColor: 'red',
        borderDash: [5, 5],
        fill: false,
      },
    ],
  };

  const capitalData = {
    labels: ['Mild', 'Moderate', 'Severe'],
    datasets: [
      {
        label: 'Capital Needs ($M)',
        data: [120, 100, 80],
        backgroundColor: ['green', 'orange', 'red'],
      },
    ],
  };

  return (
    <div>
      <h2>Customer Insights: Demand Forecasting</h2>
      <Line data={demandData} />

      <h2>Operational Efficiency: Cash Flow Forecasting</h2>
      <Line data={cashFlowData} />

      <h2>Regulatory Compliance: Capital Needs under Stress Scenarios</h2>
      <Bar data={capitalData} />
    </div>
  );
};

export default OtherGraphs;
