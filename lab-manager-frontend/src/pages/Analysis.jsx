import React, { useState } from 'react';
import AnalysisChart from '../components/Analysis/AnalysisChart';
import DataTable from '../components/Analysis/DataTable';
import '../styles/pages/Analysis.css';

const Analysis = () => {
  // 示例数据
  const sampleData = [
    {
      timestamp: '2024-03-15 14:30:00',
      temperature: 23.5,
      pressure: 101.3,
      ph: 7.2,
      status: 'Normal'
    },
    {
      timestamp: '2024-03-15 14:35:00',
      temperature: 23.7,
      pressure: 101.4,
      ph: 7.1,
      status: 'Normal'
    },
    // 更多数据...
  ];

  const [activeTab, setActiveTab] = useState('visualization');

  return (
    <div className="analysis-page">
      <div className="page-header">
        <h1>Data Analysis</h1>
        <div className="header-actions">
          <button className="btn-primary">Export Report</button>
          <button className="btn-secondary">Share Analysis</button>
        </div>
      </div>

      <div className="analysis-tabs">
        <button 
          className={`tab-button ${activeTab === 'visualization' ? 'active' : ''}`}
          onClick={() => setActiveTab('visualization')}
        >
          Visualization
        </button>
        <button 
          className={`tab-button ${activeTab === 'raw-data' ? 'active' : ''}`}
          onClick={() => setActiveTab('raw-data')}
        >
          Raw Data
        </button>
      </div>

      {activeTab === 'visualization' ? (
        <div className="charts-grid">
          <AnalysisChart 
            title="Temperature & Pressure Trends" 
            type="line"
          />
          <AnalysisChart 
            title="pH Level Distribution" 
            type="bar"
          />
          <AnalysisChart 
            title="Equipment Usage" 
            type="pie"
          />
          <AnalysisChart 
            title="Experiment Success Rate" 
            type="doughnut"
          />
        </div>
      ) : (
        <div className="data-section">
          <div className="data-filters">
            <input 
              type="text" 
              placeholder="Search data..." 
              className="search-input"
            />
            <input 
              type="date" 
              className="date-input"
            />
            <select className="filter-select">
              <option value="all">All Parameters</option>
              <option value="temperature">Temperature</option>
              <option value="pressure">Pressure</option>
              <option value="ph">pH Level</option>
            </select>
          </div>
          <DataTable data={sampleData} />
        </div>
      )}
    </div>
  );
};

export default Analysis;