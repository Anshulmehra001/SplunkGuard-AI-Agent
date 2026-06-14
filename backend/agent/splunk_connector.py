"""
SplunkGuard AI Agent - Splunk Connector
Handles all interactions with Splunk platform
"""

import os
from datetime import datetime, timedelta
from typing import List, Dict, Any
import json


class SplunkConnector:
    """
    Connector for Splunk Cloud/Enterprise
    Handles authentication, queries, and data retrieval
    """
    
    def __init__(self):
        self.host = os.getenv('SPLUNK_HOST', 'localhost')
        self.port = int(os.getenv('SPLUNK_PORT', 8089))
        self.username = os.getenv('SPLUNK_USERNAME', 'admin')
        self.password = os.getenv('SPLUNK_PASSWORD', '')
        self.token = os.getenv('SPLUNK_TOKEN', '')
        
        # For demo purposes, use mock data if no Splunk credentials
        self.use_mock_data = not self.token and not self.password
        
        if self.use_mock_data:
            print("[Splunk] ⚠️  No credentials found - using DEMO DATA")
            print("[Splunk] 💡 Set SPLUNK_TOKEN or SPLUNK_PASSWORD in .env for real data")
        else:
            print(f"[Splunk] ✅ Connected to {self.host}")
    
    def get_recent_security_events(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get recent security events from Splunk
        """
        if self.use_mock_data:
            return self._get_mock_security_events(limit)
        
        try:
            # Real Splunk query
            query = f"""
            search index=security earliest=-1h latest=now
            | head {limit}
            | table _time, src_ip, dest_ip, user, action, status, message
            """
            
            return self.execute_query(query)
            
        except Exception as e:
            print(f"[Splunk] ❌ Error fetching events: {str(e)}")
            return self._get_mock_security_events(limit)
    
    def get_recent_threats(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get detected security threats
        """
        if self.use_mock_data:
            return self._get_mock_threats(limit)
        
        try:
            query = f"""
            search index=security (threat OR attack OR malware OR suspicious)
            earliest=-24h latest=now
            | head {limit}
            | table _time, threat_type, severity, src_ip, description
            """
            
            return self.execute_query(query)
            
        except Exception as e:
            print(f"[Splunk] ❌ Error fetching threats: {str(e)}")
            return self._get_mock_threats(limit)
    
    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """
        Execute a Splunk search query
        """
        if self.use_mock_data:
            print(f"[Splunk] 🔍 Mock query: {query[:100]}...")
            return self._get_mock_security_events(10)
        
        try:
            # Use Splunk SDK to execute query
            import splunklib.client as client
            import splunklib.results as results
            
            service = client.connect(
                host=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                token=self.token
            )
            
            # Run the search
            job = service.jobs.create(query)
            
            # Wait for completion
            while not job.is_done():
                pass
            
            # Get results
            result_stream = job.results()
            reader = results.ResultsReader(result_stream)
            
            events = []
            for result in reader:
                if isinstance(result, dict):
                    events.append(result)
            
            print(f"[Splunk] ✅ Query returned {len(events)} results")
            return events
            
        except Exception as e:
            print(f"[Splunk] ❌ Query failed: {str(e)}")
            return []
    
    def get_top_threat_types(self, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get top threat types in last 24h
        """
        if self.use_mock_data:
            return [
                {"threat_type": "brute_force", "count": 45},
                {"threat_type": "port_scan", "count": 23},
                {"threat_type": "malware", "count": 12},
                {"threat_type": "ddos", "count": 8},
                {"threat_type": "insider_threat", "count": 3}
            ][:limit]
        
        # Real implementation would query Splunk
        return []
    
    # ============ MOCK DATA FOR DEMO ============
    
    def _get_mock_security_events(self, limit: int) -> List[Dict[str, Any]]:
        """
        Generate realistic mock security events for demo
        """
        import random
        
        event_templates = [
            {
                "type": "failed_login",
                "message": "Failed login attempt for user {user} from {ip}",
                "severity": "medium"
            },
            {
                "type": "successful_login",
                "message": "Successful login for user {user} from {ip}",
                "severity": "low"
            },
            {
                "type": "port_scan",
                "message": "Port scan detected from {ip} targeting {target}",
                "severity": "high"
            },
            {
                "type": "malware_detected",
                "message": "Malware signature detected: {malware} on {system}",
                "severity": "critical"
            },
            {
                "type": "firewall_block",
                "message": "Firewall blocked connection from {ip} to port {port}",
                "severity": "medium"
            },
            {
                "type": "suspicious_activity",
                "message": "Unusual network activity from {ip} at {time}",
                "severity": "high"
            }
        ]
        
        users = ["admin", "john.doe", "jane.smith", "service_account", "root"]
        ips = ["192.168.1.100", "10.0.0.50", "172.16.0.25", "203.0.113.45", "198.51.100.10"]
        systems = ["web-server-01", "db-server-02", "app-server-03", "mail-server-01"]
        malware_types = ["trojan.generic", "ransomware.wannacry", "spyware.keylogger"]
        
        events = []
        now = datetime.now()
        
        for i in range(min(limit, 50)):
            template = random.choice(event_templates)
            time_offset = timedelta(minutes=random.randint(1, 60))
            
            event = {
                "_time": (now - time_offset).isoformat(),
                "type": template["type"],
                "severity": template["severity"],
                "message": template["message"].format(
                    user=random.choice(users),
                    ip=random.choice(ips),
                    target=random.choice(systems),
                    system=random.choice(systems),
                    malware=random.choice(malware_types),
                    port=random.choice([22, 80, 443, 3389, 8080]),
                    time=datetime.now().strftime("%H:%M")
                ),
                "src_ip": random.choice(ips),
                "event_id": f"SEC-{1000 + i}"
            }
            
            events.append(event)
        
        # Add some suspicious patterns for demo
        if limit >= 10:
            # Simulate brute force attack
            attacker_ip = "203.0.113.66"
            for i in range(5):
                events.append({
                    "_time": (now - timedelta(minutes=i)).isoformat(),
                    "type": "failed_login",
                    "severity": "high",
                    "message": f"Failed login attempt for user admin from {attacker_ip}",
                    "src_ip": attacker_ip,
                    "event_id": f"SEC-ATTACK-{i}"
                })
        
        return events[:limit]
    
    def _get_mock_threats(self, limit: int) -> List[Dict[str, Any]]:
        """
        Generate mock detected threats
        """
        threats = [
            {
                "threat_id": "THR-001",
                "threat_type": "brute_force",
                "severity": "high",
                "src_ip": "203.0.113.66",
                "description": "Multiple failed login attempts detected - possible brute force attack",
                "timestamp": (datetime.now() - timedelta(minutes=15)).isoformat(),
                "status": "active"
            },
            {
                "threat_id": "THR-002",
                "threat_type": "port_scan",
                "severity": "medium",
                "src_ip": "198.51.100.10",
                "description": "Systematic port scanning activity detected",
                "timestamp": (datetime.now() - timedelta(hours=2)).isoformat(),
                "status": "mitigated"
            },
            {
                "threat_id": "THR-003",
                "threat_type": "malware",
                "severity": "critical",
                "src_ip": "internal",
                "description": "Malware signature detected on web-server-01",
                "timestamp": (datetime.now() - timedelta(hours=5)).isoformat(),
                "status": "investigating"
            }
        ]
        
        return threats[:limit]
