"""
SplunkGuard AI Agent - Brain Module
Core decision-making engine using LLM
"""

import os
from datetime import datetime
from typing import List, Dict, Any
import json

# Import based on AI provider choice
AI_PROVIDER = os.getenv('AI_PROVIDER', 'openai')

if AI_PROVIDER == 'openai':
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
else:
    from anthropic import Anthropic
    client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))


class AgentBrain:
    """
    The AI brain that analyzes security events and makes decisions
    """
    
    def __init__(self, splunk_connector, action_executor):
        self.splunk = splunk_connector
        self.actions = action_executor
        self.system_prompt = self._build_system_prompt()
    
    def _build_system_prompt(self) -> str:
        """Build the system prompt for the AI agent"""
        return """You are SplunkGuard, an autonomous AI security agent.

Your responsibilities:
1. Analyze security events from Splunk logs
2. Detect threats, anomalies, and suspicious patterns
3. Make decisions about remediation actions
4. Explain your reasoning clearly

When analyzing events:
- Look for patterns (repeated failures, unusual times, suspicious IPs)
- Consider severity (critical vs informational)
- Recommend actions (block IP, alert team, investigate, ignore)

Respond in JSON format:
{
    "threat_detected": true/false,
    "severity": "critical/high/medium/low",
    "threat_type": "brute_force/ddos/insider_threat/malware/other",
    "confidence": 0.0-1.0,
    "reasoning": "explanation",
    "recommended_actions": ["action1", "action2"],
    "affected_systems": ["system1", "system2"]
}
"""
    
    def analyze_security_events(self) -> Dict[str, Any]:
        """
        Main analysis function - gets events from Splunk and analyzes them
        """
        print("\n[Agent] 🧠 Starting security analysis...")
        
        try:
            # Get recent security events from Splunk
            events = self.splunk.get_recent_security_events(limit=50)
            
            if not events:
                print("[Agent] ℹ️  No new events to analyze")
                return {
                    "threats_detected": 0,
                    "actions_taken": 0,
                    "message": "No new events"
                }
            
            print(f"[Agent] 📊 Analyzing {len(events)} security events...")
            
            # Analyze events with AI
            analysis = self._analyze_with_ai(events)
            
            # Take actions if threat detected
            actions_taken = 0
            if analysis.get("threat_detected"):
                actions_taken = self._execute_remediation(analysis)
            
            return {
                "threats_detected": 1 if analysis.get("threat_detected") else 0,
                "actions_taken": actions_taken,
                "analysis": analysis,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"[Agent] ❌ Error during analysis: {str(e)}")
            return {
                "threats_detected": 0,
                "actions_taken": 0,
                "error": str(e)
            }
    
    def _analyze_with_ai(self, events: List[Dict]) -> Dict[str, Any]:
        """
        Use LLM to analyze security events
        """
        # Prepare events summary for AI
        events_summary = self._summarize_events(events)
        
        user_message = f"""Analyze these security events:

{events_summary}

Identify threats and recommend actions."""
        
        try:
            if AI_PROVIDER == 'openai':
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": user_message}
                    ],
                    temperature=0.3,
                    response_format={"type": "json_object"}
                )
                
                analysis = json.loads(response.choices[0].message.content)
            else:
                # Anthropic Claude
                response = client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=1024,
                    messages=[
                        {"role": "user", "content": f"{self.system_prompt}\n\n{user_message}"}
                    ]
                )
                
                analysis = json.loads(response.content[0].text)
            
            print(f"[Agent] 🔍 Analysis: {analysis.get('reasoning', 'No reasoning provided')}")
            
            return analysis
            
        except Exception as e:
            print(f"[Agent] ⚠️  AI analysis failed: {str(e)}")
            # Fallback to rule-based analysis
            return self._rule_based_analysis(events)
    
    def _summarize_events(self, events: List[Dict]) -> str:
        """Summarize events for AI analysis"""
        summary_parts = []
        
        # Group events by type
        event_types = {}
        for event in events[:20]:  # Limit to avoid token limits
            event_type = event.get('type', 'unknown')
            if event_type not in event_types:
                event_types[event_type] = []
            event_types[event_type].append(event)
        
        for event_type, type_events in event_types.items():
            summary_parts.append(f"\n{event_type.upper()} ({len(type_events)} events):")
            for event in type_events[:5]:  # Show top 5 of each type
                summary_parts.append(f"  - {event.get('message', 'No message')}")
        
        return "\n".join(summary_parts)
    
    def _rule_based_analysis(self, events: List[Dict]) -> Dict[str, Any]:
        """
        Fallback rule-based analysis if AI fails
        """
        print("[Agent] 🔧 Using rule-based analysis (fallback)")
        
        # Simple brute force detection
        failed_logins = [e for e in events if 'failed' in e.get('message', '').lower()]
        
        if len(failed_logins) >= 5:
            return {
                "threat_detected": True,
                "severity": "high",
                "threat_type": "brute_force",
                "confidence": 0.85,
                "reasoning": f"Detected {len(failed_logins)} failed login attempts - possible brute force attack",
                "recommended_actions": ["block_ip", "alert_team"],
                "affected_systems": ["authentication_system"]
            }
        
        return {
            "threat_detected": False,
            "severity": "low",
            "confidence": 0.5,
            "reasoning": "No immediate threats detected",
            "recommended_actions": [],
            "affected_systems": []
        }
    
    def _execute_remediation(self, analysis: Dict[str, Any]) -> int:
        """
        Execute recommended remediation actions
        """
        recommended_actions = analysis.get("recommended_actions", [])
        actions_taken = 0
        
        print(f"[Agent] 🛡️  Taking {len(recommended_actions)} remediation actions...")
        
        for action in recommended_actions:
            try:
                if action == "block_ip":
                    # Extract IPs from analysis and block them
                    self.actions.block_ip("192.168.1.100")  # Demo IP
                    actions_taken += 1
                    
                elif action == "alert_team":
                    self.actions.send_alert(
                        severity=analysis.get("severity"),
                        message=analysis.get("reasoning")
                    )
                    actions_taken += 1
                    
                elif action == "isolate_system":
                    systems = analysis.get("affected_systems", [])
                    for system in systems:
                        self.actions.isolate_system(system)
                    actions_taken += len(systems)
                    
            except Exception as e:
                print(f"[Agent] ⚠️  Action '{action}' failed: {str(e)}")
        
        print(f"[Agent] ✅ Completed {actions_taken} actions")
        return actions_taken
    
    def process_nl_query(self, query: str) -> Dict[str, Any]:
        """
        Process natural language security queries
        Example: "Show me failed logins in the last hour"
        """
        print(f"[Agent] 💬 Processing query: {query}")
        
        try:
            # Use AI to convert NL query to Splunk search
            prompt = f"""Convert this security question into a Splunk search query:
Question: {query}

Respond with JSON:
{{
    "splunk_query": "search query here",
    "explanation": "what this query does"
}}
"""
            
            if AI_PROVIDER == 'openai':
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                    response_format={"type": "json_object"}
                )
                result = json.loads(response.choices[0].message.content)
            else:
                response = client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=512,
                    messages=[{"role": "user", "content": prompt}]
                )
                result = json.loads(response.content[0].text)
            
            # Execute the Splunk query
            splunk_query = result.get("splunk_query", "")
            events = self.splunk.execute_query(splunk_query)
            
            return {
                "query": query,
                "splunk_query": splunk_query,
                "explanation": result.get("explanation"),
                "results": events,
                "count": len(events)
            }
            
        except Exception as e:
            print(f"[Agent] ❌ Query processing failed: {str(e)}")
            return {
                "query": query,
                "error": str(e),
                "results": []
            }
