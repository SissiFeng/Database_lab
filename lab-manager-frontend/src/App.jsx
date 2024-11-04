import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Layout/Header';
import Footer from './components/Layout/Footer';
import Sidebar from './components/Layout/Sidebar';

// 从 pages 导入页面组件
import Dashboard from './pages/Dashboard';
import Experiments from './pages/Experiments';
import Equipment from './pages/Equipment';
import Analysis from './pages/Analysis';

// 导入全局样式
import './styles/components/Layout/Header.css';
import './styles/components/Layout/Footer.css';
import './styles/components/Layout/Sidebar.css';
import './styles/pages/Equipment.css';
import './styles/pages/Dashboard.css';
import './styles/pages/Experiments.css';
import './styles/pages/Analysis.css';
import './styles/components/Dashboard/StatisticsCard.css';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app">
        <Header />
        <div className="main-container">
          <Sidebar />
          <main className="main-content">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/experiments" element={<Experiments />} />
              <Route path="/equipment" element={<Equipment />} />
              <Route path="/analysis" element={<Analysis />} />
            </Routes>
          </main>
        </div>
        <Footer />
      </div>
    </Router>
  );
}

export default App;