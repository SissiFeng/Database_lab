import React from 'react';
import '../../styles/components/Layout/Header.css';

const Header = () => {
  return (
    <header className="header">
      <div className="header-left">
        <div className="search-bar">
          <input 
            type="text" 
            placeholder="Search experiments, equipment..." 
            className="search-input"
          />
        </div>
      </div>
      
      <div className="header-right">
        <div className="notifications">
          <span className="notification-icon">🔔</span>
          <span className="notification-badge">3</span>
        </div>
        
        <div className="user-profile">
          <img 
            src="/default-avatar.png"
            alt="Profile" 
            className="avatar"
          />
          <span className="username">User</span>
        </div>
      </div>
    </header>
  );
};

export default Header;
