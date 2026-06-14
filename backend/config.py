"""
Production-ready configuration management
"""
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()


class Config:
    """Base configuration"""
    
    # Flask
    FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24).hex())
    
    # AI Provider
    AI_PROVIDER = os.getenv('AI_PROVIDER', 'openai')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
    
    # Splunk
    SPLUNK_HOST = os.getenv('SPLUNK_HOST', '')
    SPLUNK_PORT = int(os.getenv('SPLUNK_PORT', 8089))
    SPLUNK_USERNAME = os.getenv('SPLUNK_USERNAME', '')
    SPLUNK_PASSWORD = os.getenv('SPLUNK_PASSWORD', '')
    SPLUNK_TOKEN = os.getenv('SPLUNK_TOKEN', '')
    
    # Agent Configuration
    AGENT_NAME = os.getenv('AGENT_NAME', 'SplunkGuard')
    AGENT_CHECK_INTERVAL = int(os.getenv('AGENT_CHECK_INTERVAL', 30))
    MAX_EVENTS_PER_CHECK = int(os.getenv('MAX_EVENTS_PER_CHECK', 100))
    
    # Security
    AUTO_REMEDIATION_ENABLED = os.getenv('AUTO_REMEDIATION_ENABLED', 'True').lower() == 'true'
    BLOCK_IP_THRESHOLD = int(os.getenv('BLOCK_IP_THRESHOLD', 5))
    ALERT_EMAIL = os.getenv('ALERT_EMAIL', 'security@example.com')
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE = int(os.getenv('RATE_LIMIT_PER_MINUTE', 60))
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def validate(cls) -> tuple[bool, Optional[str]]:
        """Validate configuration"""
        
        # Check AI provider
        if cls.AI_PROVIDER not in ['openai', 'anthropic']:
            return False, "AI_PROVIDER must be 'openai' or 'anthropic'"
        
        # Check API keys
        if cls.AI_PROVIDER == 'openai' and not cls.OPENAI_API_KEY:
            return False, "OPENAI_API_KEY is required when using OpenAI"
        
        if cls.AI_PROVIDER == 'anthropic' and not cls.ANTHROPIC_API_KEY:
            return False, "ANTHROPIC_API_KEY is required when using Anthropic"
        
        return True, None


class DevelopmentConfig(Config):
    """Development configuration"""
    FLASK_DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    FLASK_DEBUG = False


class TestingConfig(Config):
    """Testing configuration"""
    FLASK_DEBUG = True
    TESTING = True


# Configuration dictionary
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(env: str = None) -> Config:
    """Get configuration based on environment"""
    if env is None:
        env = os.getenv('FLASK_ENV', 'development')
    
    return config_by_name.get(env, DevelopmentConfig)
