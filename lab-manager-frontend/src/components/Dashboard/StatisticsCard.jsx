import React from 'react';
import '../../styles/components/Dashboard/StatisticsCard.css';

const StatisticsCard = ({ title, value, icon, trend }) => {
  return (
    <div className="statistics-card">
      <div className="card-icon">{icon}</div>
      <div className="card-content">
        <h3 className="card-title">{title}</h3>
        <div className="card-value">{value}</div>
        {trend && (
          <div className={`card-trend ${trend > 0 ? 'positive' : 'negative'}`}>
            {trend > 0 ? '↑' : '↓'} {Math.abs(trend)}%
          </div>
        )}
      </div>
    </div>
  );
};

export default StatisticsCard;