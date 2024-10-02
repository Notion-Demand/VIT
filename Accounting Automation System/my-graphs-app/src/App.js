import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import RiskManagement from './components/RiskManagement';
import OtherGraphs from './components/OtherGraphs';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <nav>
          <ul>
            <li>
              <Link to="/">Risk Management</Link>
            </li>
            <li>
              <Link to="/other-graphs">Other Graphs</Link>
            </li>
          </ul>
        </nav>
        <Routes>
          <Route path="/" element={<RiskManagement />} />
          <Route path="/other-graphs" element={<OtherGraphs />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
