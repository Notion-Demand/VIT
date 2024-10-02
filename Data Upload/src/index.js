import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import App from './components/App';
import DataTable from './components/DataTable'; // New page for displaying the data

ReactDOM.render(
  <Router>
    <Routes>
      <Route path="/" element={<App />} />
      <Route path="/data" element={<DataTable />} />
    </Routes>
  </Router>,
  document.getElementById('root')
);
