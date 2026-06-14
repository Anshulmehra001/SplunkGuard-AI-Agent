#!/usr/bin/env python
"""
Run all tests for SplunkGuard AI Agent
"""
import sys
import unittest
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / 'backend'))

if __name__ == '__main__':
    # Discover and run tests
    loader = unittest.TestLoader()
    tests = loader.discover('backend/tests', pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(tests)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
