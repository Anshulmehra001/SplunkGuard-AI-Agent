"""
Unit tests for SplunkGuard API
"""
import unittest
import json
from app import app


class TestSplunkGuardAPI(unittest.TestCase):
    """Test cases for API endpoints"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        self.assertEqual(data['agent'], 'SplunkGuard AI')
    
    def test_agent_status(self):
        """Test agent status endpoint"""
        response = self.client.get('/api/agent/status')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('active', data)
        self.assertIn('threats_detected', data)
    
    def test_start_agent(self):
        """Test starting agent"""
        response = self.client.post('/api/agent/start')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
    
    def test_stop_agent(self):
        """Test stopping agent"""
        response = self.client.post('/api/agent/stop')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
    
    def test_get_threats(self):
        """Test getting threats"""
        response = self.client.get('/api/threats')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('threats', data)
    
    def test_dashboard_stats(self):
        """Test dashboard statistics"""
        response = self.client.get('/api/dashboard/stats')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('stats', data)
    
    def test_natural_language_query(self):
        """Test natural language query"""
        query_data = {'query': 'Show me failed logins'}
        response = self.client.post(
            '/api/query',
            data=json.dumps(query_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
    
    def test_invalid_query(self):
        """Test invalid query (missing query field)"""
        response = self.client.post(
            '/api/query',
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
