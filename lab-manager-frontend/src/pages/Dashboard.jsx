import React from 'react';
import StatisticsCard from '../components/Dashboard/StatisticsCard';
import '../styles/pages/Dashboard.css';  // 修改导入路径

const Dashboard = () => {
  const statistics = [
    {
      title: "Active Experiments",
      value: "12",
      icon: "🧪",
      trend: 8
    },
    {
      title: "Equipment Online",
      value: "24/25",
      icon: "⚡",
      trend: 4
    },
    {
      title: "Data Points Today",
      value: "1,284",
      icon: "📊",
      trend: 12
    },
    {
      title: "Alerts",
      value: "2",
      icon: "⚠️",
      trend: -50
    }
  ];

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Dashboard</h1>
        <div className="header-actions">
          <button className="btn-primary">New Experiment</button>
          <button className="btn-secondary">Export Report</button>
        </div>
      </div>

      <div className="statistics-grid">
        {statistics.map((stat, index) => (
          <StatisticsCard
            key={index}
            title={stat.title}
            value={stat.value}
            icon={stat.icon}
            trend={stat.trend}
          />
        ))}
      </div>
    </div>
  );
};

export default Dashboard;