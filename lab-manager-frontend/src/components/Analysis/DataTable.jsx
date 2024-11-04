import React from 'react';
import '../../styles/components/Analysis/DataTable.css';

const DataTable = ({ data }) => {
  return (
    <div className="data-table">
      <table>
        <thead>
          <tr>
            <th>Timestamp</th>
            <th>Temperature (°C)</th>
            <th>Pressure (kPa)</th>
            <th>pH Level</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {data.map((row, index) => (
            <tr key={index}>
              <td>{row.timestamp}</td>
              <td>{row.temperature}</td>
              <td>{row.pressure}</td>
              <td>{row.ph}</td>
              <td>
                <span className={`status-badge ${row.status.toLowerCase()}`}>
                  {row.status}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default DataTable;