import React, { useState, useEffect } from 'react';
import './App.css';
import Dashboard from './components/Dashboard';
import ChatInterface from './components/ChatInterface';
import ThreatsList from './components/ThreatsList';
import * as api from './api';

function App() {
  const [agentStatus, setAgentStatus] = useState({
    active: false,
    threats_detected: 0,
    actions_taken: 0
  });
  const [stats, setStats] = useState(null);
  const [threats, setThreats] = useState([]);
  const [loading, setLoading] = useState(false);

  // Load initial data
  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 10000); // Refresh every 10s
    return () => clearInterval(interval);
  }, []);

  const loadData = async () => {
    try {
      const [statusData, statsData, threatsData] = await Promise.all([
        api.getAgentStatus(),
        api.getDashboardStats(),
        api.getThreats()
      ]);
      
      setAgentStatus(statusData);
      setStats(statsData.stats);
      setThreats(threatsData.threats || []);
    } catch (error) {
      console.error('Error loading data:', error);
    }
  };

  const startAgent = async () => {
    setLoading(true);
    try {
      const result = await api.startAgent();
      setAgentStatus(result.status);
      await loadData();
    } catch (error) {
      console.error('Error starting agent:', error);
      alert('Failed to start agent. Check console for details.');
    } finally {
      setLoading(false);
    }
  };

  const stopAgent = async () => {
    setLoading(true);
    try {
      const result = await api.stopAgent();
      setAgentStatus(result.status);
    } catch (error) {
      console.error('Error stopping agent:', error);
    } finally {
      setLoading(false);
    }
  };

  const analyzeNow = async () => {
    setLoading(true);
    try {
      const result = await api.analyzeNow();
      setAgentStatus(result.status);
      await loadData();
    } catch (error) {
      console.error('Error analyzing:', error);
      alert('Analysis failed. Check console for details.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <div className="header-content">
          <div className="logo-section">
            <div className="logo">🛡️</div>
            <div>
              <h1>SplunkGuard AI Agent</h1>
              <p className="subtitle">Autonomous Security Monitoring & Response</p>
            </div>
          </div>
          
          <div className="agent-controls">
            <div className={`status-indicator ${agentStatus.active ? 'active' : 'inactive'}`}>
              <span className="status-dot"></span>
              {agentStatus.active ? 'Agent Active' : 'Agent Stopped'}
            </div>
            
            {!agentStatus.active ? (
              <button 
                className="btn btn-primary" 
                onClick={startAgent}
                disabled={loading}
              >
                {loading ? 'Starting...' : '▶ Start Agent'}
              </button>
            ) : (
              <>
                <button 
                  className="btn btn-secondary" 
                  onClick={analyzeNow}
                  disabled={loading}
                >
                  🔍 Analyze Now
                </button>
                <button 
                  className="btn btn-danger" 
                  onClick={stopAgent}
                  disabled={loading}
                >
                  ⏹ Stop Agent
                </button>
              </>
            )}
          </div>
        </div>
      </header>

      <main className="App-main">
        <Dashboard stats={stats} agentStatus={agentStatus} />
        
        <div className="grid-2">
          <ChatInterface />
          <ThreatsList threats={threats} />
        </div>
      </main>

      <footer className="App-footer">
        <p>SplunkGuard AI Agent v1.0 | Enterprise Security Automation</p>
      </footer>
    </div>
  );
}

export default App;
