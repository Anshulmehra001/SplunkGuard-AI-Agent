"""
SplunkGuard AI Agent - Action Executor
Handles remediation actions (block IPs, send alerts, isolate systems)
"""

import os
from datetime import datetime
from typing import List, Dict, Any


class ActionExecutor:
    """
    Executes security remediation actions
    """
    
    def __init__(self):
        self.auto_remediation = os.getenv('AUTO_REMEDIATION_ENABLED', 'True').lower() == 'true'
        self.alert_email = os.getenv('ALERT_EMAIL', 'security@example.com')
        
        # Store action history
        self.action_history = []
        self.blocked_ips = set()
        self.alerts_sent = 0
        
        print(f"[Actions] 🛡️  Auto-remediation: {'ENABLED' if self.auto_remediation else 'DISABLED'}")
    
    def block_ip(self, ip_address: str, reason: str = "Suspicious activity") -> bool:
        """
        Block an IP address at the firewall
        """
        try:
            print(f"[Actions] 🚫 Blocking IP: {ip_address}")
            print(f"[Actions]    Reason: {reason}")
            
            if not self.auto_remediation:
                print("[Actions] ⚠️  Auto-remediation disabled - would block in production")
                return False
            
            # In production, this would call firewall API
            # Example: AWS Security Groups, Cloudflare, iptables, etc.
            
            # For demo: just record the action
            self.blocked_ips.add(ip_address)
            self._record_action("block_ip", {
                "ip": ip_address,
                "reason": reason
            })
            
            print(f"[Actions] ✅ IP {ip_address} blocked successfully")
            return True
            
        except Exception as e:
            print(f"[Actions] ❌ Failed to block IP: {str(e)}")
            return False
    
    def send_alert(self, severity: str, message: str, recipients: List[str] = None) -> bool:
        """
        Send security alert to team
        """
        try:
            recipients = recipients or [self.alert_email]
            
            print(f"[Actions] 📧 Sending {severity.upper()} alert")
            print(f"[Actions]    To: {', '.join(recipients)}")
            print(f"[Actions]    Message: {message}")
            
            # In production: send email, Slack, PagerDuty, etc.
            # Example integrations:
            # - SendGrid/AWS SES for email
            # - Slack webhooks
            # - PagerDuty API
            # - Microsoft Teams
            
            self.alerts_sent += 1
            self._record_action("send_alert", {
                "severity": severity,
                "message": message,
                "recipients": recipients
            })
            
            print("[Actions] ✅ Alert sent successfully")
            return True
            
        except Exception as e:
            print(f"[Actions] ❌ Failed to send alert: {str(e)}")
            return False
    
    def isolate_system(self, system_name: str) -> bool:
        """
        Isolate a compromised system from network
        """
        try:
            print(f"[Actions] 🔒 Isolating system: {system_name}")
            
            if not self.auto_remediation:
                print("[Actions] ⚠️  Auto-remediation disabled - would isolate in production")
                return False
            
            # In production: remove from network, disable network interface
            # Example: AWS Security Groups, VMware network isolation
            
            self._record_action("isolate_system", {
                "system": system_name,
                "timestamp": datetime.now().isoformat()
            })
            
            print(f"[Actions] ✅ System {system_name} isolated")
            return True
            
        except Exception as e:
            print(f"[Actions] ❌ Failed to isolate system: {str(e)}")
            return False
    
    def kill_process(self, system: str, process_id: int, process_name: str) -> bool:
        """
        Kill a malicious process
        """
        try:
            print(f"[Actions] ⚠️  Killing process {process_name} (PID: {process_id}) on {system}")
            
            if not self.auto_remediation:
                print("[Actions] ⚠️  Auto-remediation disabled")
                return False
            
            # In production: use remote execution tools
            # Example: SSH, WinRM, Ansible, Puppet
            
            self._record_action("kill_process", {
                "system": system,
                "process_id": process_id,
                "process_name": process_name
            })
            
            print("[Actions] ✅ Process killed")
            return True
            
        except Exception as e:
            print(f"[Actions] ❌ Failed to kill process: {str(e)}")
            return False
    
    def quarantine_file(self, system: str, file_path: str) -> bool:
        """
        Quarantine a malicious file
        """
        try:
            print(f"[Actions] 🗂️  Quarantining file: {file_path} on {system}")
            
            # Move file to quarantine directory
            self._record_action("quarantine_file", {
                "system": system,
                "file_path": file_path
            })
            
            print("[Actions] ✅ File quarantined")
            return True
            
        except Exception as e:
            print(f"[Actions] ❌ Failed to quarantine file: {str(e)}")
            return False
    
    def _record_action(self, action_type: str, details: Dict[str, Any]):
        """
        Record action in history
        """
        action_record = {
            "id": len(self.action_history) + 1,
            "timestamp": datetime.now().isoformat(),
            "type": action_type,
            "details": details,
            "status": "completed"
        }
        
        self.action_history.append(action_record)
    
    def get_action_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get action history
        """
        return self.action_history[-limit:]
    
    def get_blocked_ips_count(self) -> int:
        """
        Get count of blocked IPs
        """
        return len(self.blocked_ips)
    
    def get_alerts_count(self) -> int:
        """
        Get count of alerts sent
        """
        return self.alerts_sent
    
    def get_blocked_ips(self) -> List[str]:
        """
        Get list of blocked IPs
        """
        return list(self.blocked_ips)
