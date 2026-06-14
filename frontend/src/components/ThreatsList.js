import React from 'react';
import './ThreatsList.css';

function ThreatsList({ threats }) {
  const getSeverityClass = (severity) => {
    const severityMap = {
      critical: 'critical',
      high: 'high',
      medium: 'medium',
      low: 'low'
    };
    return severityMap[severity?.toLowerCase()] || 'medium';
  };

  const getThreatIcon = (threatType) => {
    const icons = {
      brute_force: '🔓',
      port_scan: '🔍',
      malware: '🦠',
      ddos: '💥',
      insider_threat: '👤',
      suspicious_activity: '⚠️',
      default: '🚨'
    };
    return icons[threatType] || icons.default;
  };

  return (
    <div className="threats-list">
      <h2>🚨 Recent Threats</h2>
      
      {threats.length === 0 ? (
        <div className="no-threats">
          <div className="no-threats-icon">✅</div>
          <p>No active threats detected</p>
          <small>Your systems are secure</small>
        </div>
      ) : (
        <div className="threats-container">
          {threats.map((threat, index) => (
            <div key={index} className={`threat-item ${getSeverityClass(threat.severity)}`}>
              <div className="threat-header">
                <span className="threat-icon">
                  {getThreatIcon(threat.threat_type)}
                </span>
                <div className="threat-title">
                  <h3>{threat.threat_type?.replace('_', ' ') || 'Security Event'}</h3>
                  <span className={`severity-badge ${getSeverityClass(threat.severity)}`}>
                    {threat.severity || 'medium'}
                  </span>
                </div>
              </div>
              
              <p className="threat-description">
                {threat.description || threat.message || 'Security threat detected'}
              </p>
              
              <div className="threat-details">
                {threat.src_ip && (
                  <div className="threat-detail">
                    <span className="detail-label">Source IP:</span>
                    <code>{threat.src_ip}</code>
                  </div>
                )}
                
                {threat.timestamp && (
                  <div className="threat-detail">
                    <span className="detail-label">Time:</span>
                    <span>{new Date(threat.timestamp).toLocaleString()}</span>
                  </div>
                )}
                
                {threat.status && (
                  <div className="threat-detail">
                    <span className="detail-label">Status:</span>
                    <span className={`status-pill ${threat.status}`}>
                      {threat.status}
                    </span>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default ThreatsList;
