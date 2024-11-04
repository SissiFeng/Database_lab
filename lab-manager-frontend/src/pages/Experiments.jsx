import React from 'react';
import '../styles/pages/Experiments.css';

const Experiments = () => {
  return (
    <div className="experiments-page">
      <div className="page-header">
        <h1>Experiments</h1>
        <div className="header-actions">
          <button className="btn-primary">New Experiment</button>
          <button className="btn-secondary">Import Data</button>
        </div>
      </div>

      <div className="filters">
        <input 
          type="text" 
          placeholder="Search experiments..." 
          className="search-input"
        />
        <select className="filter-select">
          <option value="all">All Status</option>
          <option value="ongoing">Ongoing</option>
          <option value="completed">Completed</option>
          <option value="planned">Planned</option>
        </select>
        <select className="filter-select">
          <option value="all">All Types</option>
          <option value="chemical">Chemical</option>
          <option value="biological">Biological</option>
          <option value="physical">Physical</option>
        </select>
      </div>

      <div className="experiments-grid">
        {/* 示例实验卡片 */}
        <div className="experiment-card">
          <div className="card-header">
            <h3>Protein Analysis #127</h3>
            <span className="status-badge status-ongoing">Ongoing</span>
          </div>
          <div className="card-content">
            <p className="experiment-desc">Analysis of protein structures in sample B-234</p>
            <div className="experiment-meta">
              <div className="meta-item">
                <span className="label">Start Date:</span>
                <span>2024-03-15</span>
              </div>
              <div className="meta-item">
                <span className="label">Duration:</span>
                <span>5 days</span>
              </div>
              <div className="meta-item">
                <span className="label">Researcher:</span>
                <span>Dr. Smith</span>
              </div>
            </div>
          </div>
          <div className="card-actions">
            <button className="btn-icon">📊</button>
            <button className="btn-icon">📝</button>
            <button className="btn-icon">🔬</button>
          </div>
        </div>

        {/* 可以添加更多实验卡片 */}
      </div>
    </div>
  );
};

export default Experiments;