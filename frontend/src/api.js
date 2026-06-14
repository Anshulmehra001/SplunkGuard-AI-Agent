/**
 * API client for SplunkGuard backend
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';
const USE_DEMO_MODE = true; // Enable demo mode when backend is unavailable

// Demo data for when backend is not available
const DEMO_DATA = {
  agentStatus: {
    active: false,
    threats_detected: 127,
    actions_taken: 89,
    last_check: new Date().toISOString()
  },
  stats: {
    last_24h: {
      threats_detected: 23,
      actions_taken: 18,
      blocked_ips: 12,
      alerts_sent: 15
    },
    top_threats: [
      { threat_type: 'brute_force', count: 8 },
      { threat_type: 'suspicious_login', count: 6 },
      { threat_type: 'malware_detected', count: 5 },
      { threat_type: 'data_exfiltration', count: 4 }
    ]
  },
  threats: [
    {
      id: '1',
      timestamp: new Date(Date.now() - 1000 * 60 * 15).toISOString(),
      severity: 'critical',
      threat_type: 'Brute Force Attack',
      source_ip: '192.168.1.104',
      target: 'SSH Server',
      description: 'Multiple failed login attempts detected from 192.168.1.104',
      action_taken: 'IP Blocked',
      status: 'resolved'
    },
    {
      id: '2',
      timestamp: new Date(Date.now() - 1000 * 60 * 45).toISOString(),
      severity: 'high',
      threat_type: 'Suspicious Login',
      source_ip: '10.0.0.45',
      target: 'Admin Portal',
      description: 'Login from unusual location detected',
      action_taken: 'Alert Sent',
      status: 'investigating'
    },
    {
      id: '3',
      timestamp: new Date(Date.now() - 1000 * 60 * 120).toISOString(),
      severity: 'medium',
      threat_type: 'Port Scan',
      source_ip: '172.16.0.88',
      target: 'Network Gateway',
      description: 'Systematic port scanning activity detected',
      action_taken: 'Monitored',
      status: 'monitoring'
    }
  ],
  actionHistory: [
    { timestamp: new Date().toISOString(), action: 'Blocked IP 192.168.1.104', result: 'success' },
    { timestamp: new Date().toISOString(), action: 'Sent alert to security team', result: 'success' }
  ]
};

async function fetchAPI(endpoint, options = {}) {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'API request failed');
    }

    return data;
  } catch (error) {
    console.error(`API Error (${endpoint}):`, error);
    
    // Return demo data if backend is unavailable
    if (USE_DEMO_MODE) {
      console.warn('Using demo data - backend unavailable');
      return getDemoData(endpoint);
    }
    
    throw error;
  }
}

function getDemoData(endpoint) {
  // Simulate API delay
  return new Promise(resolve => {
    setTimeout(() => {
      if (endpoint.includes('/agent/status')) {
        resolve(DEMO_DATA.agentStatus);
      } else if (endpoint.includes('/dashboard/stats')) {
        resolve({ stats: DEMO_DATA.stats });
      } else if (endpoint.includes('/threats')) {
        resolve({ threats: DEMO_DATA.threats });
      } else if (endpoint.includes('/actions/history')) {
        resolve({ actions: DEMO_DATA.actionHistory });
      } else if (endpoint.includes('/agent/start')) {
        resolve({ status: { ...DEMO_DATA.agentStatus, active: true }, message: 'Demo mode - agent started' });
      } else if (endpoint.includes('/agent/stop')) {
        resolve({ status: { ...DEMO_DATA.agentStatus, active: false }, message: 'Demo mode - agent stopped' });
      } else if (endpoint.includes('/analyze')) {
        resolve({ status: DEMO_DATA.agentStatus, message: 'Demo mode - analysis simulated' });
      } else if (endpoint.includes('/query')) {
        resolve({ 
          response: 'Demo mode: I can see you have 23 threats in the last 24 hours. The most common threat type is brute force attacks. I recommend reviewing the blocked IPs list.',
          thinking: 'Analyzing security data...',
          timestamp: new Date().toISOString()
        });
      } else {
        resolve({ message: 'Demo mode active' });
      }
    }, 500);
  });
}

export async function getAgentStatus() {
  return fetchAPI('/agent/status');
}

export async function startAgent() {
  return fetchAPI('/agent/start', { method: 'POST' });
}

export async function stopAgent() {
  return fetchAPI('/agent/stop', { method: 'POST' });
}

export async function analyzeNow() {
  return fetchAPI('/analyze', { method: 'POST' });
}

export async function getThreats() {
  return fetchAPI('/threats');
}

export async function getDashboardStats() {
  return fetchAPI('/dashboard/stats');
}

export async function getActionHistory() {
  return fetchAPI('/actions/history');
}

export async function sendQuery(query) {
  return fetchAPI('/query', {
    method: 'POST',
    body: JSON.stringify({ query }),
  });
}
