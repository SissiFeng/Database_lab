import React from 'react';
import '../../styles/components/Equipment/EquipmentList.css';

const EquipmentList = () => {
  const equipment = [
    {
      id: "EQ001",
      name: "Microscope XR-500",
      status: "Online",
      lastMaintenance: "2024-03-01",
      nextMaintenance: "2024-04-01",
      usage: 75,
      temperature: 23.5,
      location: "Lab Room A"
    },
    {
      id: "EQ002",
      name: "Centrifuge CT-200",
      status: "In Use",
      lastMaintenance: "2024-02-15",
      nextMaintenance: "2024-03-15",
      usage: 45,
      temperature: 22.1,
      location: "Lab Room B"
    },
    // 更多设备...
  ];

  const getStatusColor = (status) => {
    const colors = {
      'Online': 'status-online',
      'Offline': 'status-offline',
      'In Use': 'status-in-use',
      'Maintenance': 'status-maintenance'
    };
    return colors[status] || '';
  };

  return (
    <div className="equipment-list">
      <div className="equipment-grid">
        {equipment.map((item) => (
          <div key={item.id} className="equipment-card">
            <div className="card-header">
              <h3>{item.name}</h3>
              <span className={`status-badge ${getStatusColor(item.status)}`}>
                {item.status}
              </span>
            </div>
            
            <div className="card-body">
              <div className="info-row">
                <span className="label">ID:</span>
                <span>{item.id}</span>
              </div>
              <div className="info-row">
                <span className="label">Location:</span>
                <span>{item.location}</span>
              </div>
              <div className="info-row">
                <span className="label">Temperature:</span>
                <span>{item.temperature}°C</span>
              </div>
              
              <div className="usage-section">
                <div className="usage-label">
                  <span>Usage</span>
                  <span>{item.usage}%</span>
                </div>
                <div className="usage-bar">
                  <div 
                    className="usage-fill"
                    style={{ width: `${item.usage}%` }}
                  />
                </div>
              </div>

              <div className="maintenance-info">
                <div>
                  <small>Last Maintenance</small>
                  <div>{item.lastMaintenance}</div>
                </div>
                <div>
                  <small>Next Maintenance</small>
                  <div>{item.nextMaintenance}</div>
                </div>
              </div>
            </div>

            <div className="card-actions">
              <button className="btn-icon" title="Monitor">📊</button>
              <button className="btn-icon" title="Settings">⚙️</button>
              <button className="btn-icon" title="Maintenance">🔧</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default EquipmentList;