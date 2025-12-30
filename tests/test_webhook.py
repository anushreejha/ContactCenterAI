"""
Unit tests for Dialogflow webhook.
"""

import json
import pytest
from cloudfunctions.webhook.main import webhook, get_order_status, format_order_response


class MockRequest:
    """Mock Flask request for testing."""
    def __init__(self, json_data):
        self._json = json_data
    
    def get_json(self, silent=False):
        return self._json


def test_order_tracking_success():
    """Test successful order tracking."""
    request_data = {
        'fulfillmentInfo': {'tag': 'order_tracking'},
        'sessionInfo': {
            'parameters': {'order_id': 'ORD-12345'}
        }
    }
    
    request = MockRequest(request_data)
    response = webhook(request)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'in transit' in data['fulfillment_response']['messages'][0]['text']['text'][0].lower()


def test_order_not_found():
    """Test order not found scenario."""
    order_data = get_order_status('INVALID-ID')
    assert order_data['status'] == 'not_found'
    
    response = format_order_response(order_data, 'INVALID-ID')
    assert "couldn't find" in response.lower()


def test_faq_handler():
    """Test FAQ responses."""
    request_data = {
        'fulfillmentInfo': {'tag': 'faq_handler'},
        'sessionInfo': {
            'parameters': {'faq_type': 'shipping'}
        }
    }
    
    request = MockRequest(request_data)
    response = webhook(request)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'shipping' in data['fulfillment_response']['messages'][0]['text']['text'][0].lower()
