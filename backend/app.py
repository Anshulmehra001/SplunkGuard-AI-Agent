"""
SplunkGuard AI Agent - Main Flask Application
Handles API endpoints for the AI agent and frontend
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
from datetime import datetime

from agent.brain import AgentBrain
from agent.splunk_connector import SplunkConnector
from agent.actions import ActionExecutor

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize components
splunk = SplunkConnector()
action_executor = ActionExecutor()
agent_brain = AgentBrain(splunk, action_executor)

# Store recent activity for dashboard
recent_activity = []
agent_status = {
    "active": False,
    "last_check": None,
    "threats_detected": 0,
    "actions_taken": 0
}


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "agent": "SplunkGuard AI",
        "version": "1.0.0"
    })


@app.route('/api/agent/start', methods=['POST'])
def start_agent():
    """Start the AI agent monitoring"""
    global agent_status
    
    try:
        agent_status["active"] = True
        agent_status["last_check"] = datetime.now().isoformat()
        
        # Start agent in background (simplified for demo)
        result = agent_brain.analyze_security_events()
        
        return jsonify({
            "success": True,
            "message": "Agent started successfully",
            "status": agent_status
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/agent/stop', methods=['POST'])
def stop_agent():
    """Stop the AI agent monitoring"""
    global agent_status
    
    agent_status["active"] = False
    
    return jsonify({
        "success": True,
        "message": "Agent stopped",
        "status": agent_status
    })


@app.route('/api/agent/status', methods=['GET'])
def get_agent_status():
    """Get current agent status"""
    return jsonify(agent_status)


@app.route('/api/threats', methods=['GET'])
def get_threats():
    """Get recent security threats detected"""
    try:
        # Get threats from Splunk
        threats = splunk.get_recent_threats(limit=50)
        
        return jsonify({
            "success": True,
            "count": len(threats),
            "threats": threats
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/analyze', methods=['POST'])
def analyze_now():
    """Trigger immediate analysis"""
    global agent_status
    
    try:
        result = agent_brain.analyze_security_events()
        
        agent_status["threats_detected"] += result.get("threats_detected", 0)
        agent_status["actions_taken"] += result.get("actions_taken", 0)
        agent_status["last_check"] = datetime.now().isoformat()
        
        return jsonify({
            "success": True,
            "result": result,
            "status": agent_status
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/query', methods=['POST'])
def natural_language_query():
    """Natural language security query interface"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        if not query:
            return jsonify({
                "success": False,
                "error": "Query is required"
            }), 400
        
        # Process natural language query
        result = agent_brain.process_nl_query(query)
        
        return jsonify({
            "success": True,
            "query": query,
            "response": result
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/actions/history', methods=['GET'])
def get_action_history():
    """Get history of actions taken by agent"""
    try:
        history = action_executor.get_action_history(limit=100)
        
        return jsonify({
            "success": True,
            "count": len(history),
            "actions": history
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    """Get dashboard statistics"""
    try:
        stats = {
            "agent_status": agent_status,
            "last_24h": {
                "threats_detected": agent_status["threats_detected"],
                "actions_taken": agent_status["actions_taken"],
                "blocked_ips": action_executor.get_blocked_ips_count(),
                "alerts_sent": action_executor.get_alerts_count()
            },
            "top_threats": splunk.get_top_threat_types(limit=5),
            "recent_activity": recent_activity[-10:]  # Last 10 activities
        }
        
        return jsonify({
            "success": True,
            "stats": stats
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"""
    ╔═══════════════════════════════════════════╗
    ║   SplunkGuard AI Agent - Backend Server   ║
    ║   Running on http://localhost:{port}       ║
    ╚═══════════════════════════════════════════╝
    """)
    
    app.run(host='0.0.0.0', port=port, debug=debug)
