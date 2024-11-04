import React from 'react';
import { NavLink } from 'react-router-dom';
import '../../styles/components/Layout/Sidebar.css';

const Sidebar = () => {
  const menuItems = [
    { icon: '📊', label: 'Dashboard', path: '/dashboard' },
    { icon: '🧪', label: 'Experiments', path: '/experiments' },
    { icon: '⚡', label: 'Equipment', path: '/equipment' },
    { icon: '📈', label: 'Analysis', path: '/analysis' },
    { icon: '⚙️', label: 'Settings', path: '/settings' },
  ];

  return (
    <aside className="sidebar">
      <div className="logo-container">
        <h1 className="logo">Lab Manager</h1>
      </div>

      <nav className="nav-menu">
        {menuItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) => 
              `nav-item ${isActive ? 'active' : ''}`
            }
          >
            <span className="nav-icon">{item.icon}</span>
            <span className="nav-label">{item.label}</span>
          </NavLink>
        ))}
      </nav>

      <div className="sidebar-footer">
        <div className="lab-status">
          <span className="status-dot online"></span>
          <span className="status-text">All Systems Online</span>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;