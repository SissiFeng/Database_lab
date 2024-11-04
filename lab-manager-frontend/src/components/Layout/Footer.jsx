import React from 'react';
import '../../styles/components/Layout/Footer.css';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-content">
        <div className="footer-left">
          <span className="system-status">
            System Status: <span className="status-text">Operational</span>
          </span>
        </div>
        
        <div className="footer-center">
          <span className="last-sync">
            Last Sync: {new Date().toLocaleTimeString()}
          </span>
        </div>
        
        <div className="footer-right">
          <span className="version">v1.0.0</span>
        </div>
      </div>
    </footer>
  );
};

export default Footer;