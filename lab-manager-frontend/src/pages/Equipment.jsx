import React from 'react';
import EquipmentList from '../components/Equipment/EquipmentList';
import '../styles/pages/Equipment.css';

const Equipment = () => {
  console.log('Equipment component rendered');

  return (
    <div className="equipment-page">
      <div className="page-header">
        <h1>Equipment</h1>
        <div className="header-actions">
          <button className="btn-primary">Add Equipment</button>
          <button className="btn-secondary">Generate Report</button>
        </div>
      </div>

      <div style={{ color: 'red', marginBottom: '20px' }}>
        Test Content - If you can see this, the Equipment component is rendering
      </div>

      <div className="filters">
        <input 
          type="text" 
          placeholder="Search equipment..." 
          className="search-input"
        />
        <select className="filter-select">
          <option value="all">All Status</option>
          <option value="online">Online</option>
          <option value="offline">Offline</option>
          <option value="in-use">In Use</option>
          <option value="maintenance">Maintenance</option>
        </select>
        <select className="filter-select">
          <option value="all">All Locations</option>
          <option value="lab-a">Lab Room A</option>
          <option value="lab-b">Lab Room B</option>
          <option value="lab-c">Lab Room C</option>
        </select>
      </div>

      <EquipmentList />
    </div>
  );
};

export default Equipment;