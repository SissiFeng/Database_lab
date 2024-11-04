import React from 'react';
import '../../styles/components/Experiments/ExperimentList.css';

const ExperimentList = () => {
  const experiments = [
    {
      id: "EXP001",
      name: "Temperature Sensitivity Analysis",
      status: "Running",
      startDate: "2024-03-15",
      researcher: "John Smith",
      progress: 68
    },
    {
      id: "EXP002",
      name: "Catalyst Efficiency Test",
      status: "Completed",
      startDate: "2024-03-10",
      researcher: "Emma Davis",
      progress: 100
    },
    // 更多实验数据...
  ];

  const getStatusColor = (status) => {
    const colors = {
      'Running': 'status-running',
      'Completed': 'status-completed',
      'Paused': 'status-paused',
      'Failed': 'status-failed'
    };
    return colors[status] || '';
  };

  return (
    <div className="experiment-list">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Status</th>
            <th>Start Date</th>
            <th>Researcher</th>
            <th>Progress</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {experiments.map((experiment) => (
            <tr key={experiment.id}>
              <td>{experiment.id}</td>
              <td>{experiment.name}</td>
              <td>
                <span className={`status-badge ${getStatusColor(experiment.status)}`}>
                  {experiment.status}
                </span>
              </td>
              <td>{experiment.startDate}</td>
              <td>{experiment.researcher}</td>
              <td>
                <div className="progress-bar">
                  <div 
                    className="progress-fill"
                    style={{ width: `${experiment.progress}%` }}
                  />
                  <span>{experiment.progress}%</span>
                </div>
              </td>
              <td>
                <div className="action-buttons">
                  <button className="btn-icon" title="View Details">👁️</button>
                  <button className="btn-icon" title="Edit">✏️</button>
                  <button className="btn-icon" title="Delete">🗑️</button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ExperimentList;