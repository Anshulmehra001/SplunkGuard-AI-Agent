import React from 'react';
import './Dashboard.css';

function Dashboard({ stats, agentStatus }) {
  if (!stats) {
    return (
      <div className="dashboard">
        <div className="loading">Loading dashboard...</div>
      </div>
    );
  }

  const last24h = stats.last_24h || {};

  return (
    <div className="dashboard">
      <h2>📊 Dashboard</h2>
      
      <div className="stats-grid">
        <div className="stat-card threats">
          <div className="stat-icon">⚠️</div>
          <div className="stat-content">
            <div className="stat-value">{last24h.threats_detected || 0}</div>
            <div className="stat-label">Threats Detected</div>
            <div className="stat-period">Last 24 hours</div>
          </div>
        </div>

        <div className="stat-card actions">
          <div className="stat-icon">🛡️</div>
          <div className="stat-content">
            <div className="stat-value">{last24h.actions_taken || 0}</div>
            <div className="stat-label">Actions Taken</div>
            <div className="stat-period">Automated responses</div>
          </div>
        </div>

        <div className="stat-card blocked">
          <div className="stat-icon">🚫</div>
          <div className="stat-content">
            <div className="stat-value">{last24h.blocked_ips || 0}</div>
            <div className="stat-label">IPs Blocked</div>
            <div className="stat-period">Security perimeter</div>
          </div>
        </div>

        <div className="stat-card alerts">
          <div className="stat-icon">📧</div>
          <div className="stat-content">
            <div className="stat-value">{last24h.alerts_sent || 0}</div>
            <div className="stat-label">Alerts Sent</div>
            <div className="stat-period">Team notifications</div>
          </div>
        </div>
      </div>

      {stats.top_threats && stats.top_threats.length > 0 && (
        <div className="top-threats">
          <h3>🔝 Top Threat Types</h3>
          <div className="threat-types-list">
            {stats.top_threats.map((threat, index) => (
              <div key={index} className="threat-type-item">
                <span className="threat-name">{threat.threat_type.replace('_', ' ')}</span>
                <span className="threat-count">{threat.count}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default Dashboard;
