"""
Dialogflow CX Webhook for ContactCenterAI
Handles order tracking and FAQ fulfillment.

Author: Anushree Jha
"""

import json
import logging
import os
from datetime import datetime
from typing import Any, Dict

import functions_framework
from flask import Request, jsonify

# Configure logging (Google Cloud Logging format)
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

# Environment configuration
PROJECT_ID = os.environ.get('PROJECT_ID', 'demo-project')
ORDER_API_URL = os.environ.get('ORDER_API_URL', 'https://api.example.com/orders')


# ========== Helper Functions ==========

def get_order_status(order_id: str) -> Dict[str, Any]:
    """
    Fetch order status from backend API.
    
    Args:
        order_id: Order identifier (e.g., ORD-12345)
        
    Returns:
        Dictionary with order details
        
    Note: In production, replace with actual API call
    """
    # Mock data for demonstration
    mock_orders = {
        'ORD-12345': {
            'status': 'in_transit',
            'expected_delivery': '2025-12-28',
            'carrier': 'FedEx',
            'tracking_number': '1234567890'
        },
        'ORD-67890': {
            'status': 'delivered',
            'delivery_date': '2025-12-20',
            'signed_by': 'Customer'
        }
    }
    
    return mock_orders.get(order_id, {'status': 'not_found'})


def format_order_response(order_data: Dict[str, Any], order_id: str) -> str:
    """
    Generate user-friendly order status message.
    
    Args:
        order_data: Order information dictionary
        order_id: Order identifier
        
    Returns:
        Formatted response string
    """
    status = order_data.get('status')
    
    if status == 'not_found':
        return f"I couldn't find an order with ID {order_id}. Please check the order number and try again."
    
    if status == 'in_transit':
        expected = order_data.get('expected_delivery', 'unknown')
        carrier = order_data.get('carrier', 'our carrier')
        return (
            f"Your order {order_id} is currently in transit with {carrier}. "
            f"Expected delivery: {expected}. Would you like tracking details?"
        )
    
    if status == 'delivered':
        delivery_date = order_data.get('delivery_date', 'recently')
        return f"Your order {order_id} was successfully delivered on {delivery_date}."
    
    return f"Your order {order_id} status: {status}"


def get_faq_response(question_type: str) -> str:
    """
    Retrieve FAQ responses.
    
    Args:
        question_type: Type of FAQ (shipping, returns, refunds, etc.)
        
    Returns:
        FAQ answer string
    """
    faqs = {
        'shipping': (
            "We offer free standard shipping (5-7 business days) on orders over $50. "
            "Express shipping (2-3 days) is available for $9.99."
        ),
        'returns': (
            "We accept returns within 30 days of purchase for unused items in original packaging. "
            "Return shipping is free for defective items."
        ),
        'refunds': (
            "Refunds are processed within 5-7 business days after we receive your return. "
            "The amount will be credited to your original payment method."
        ),
        'payment': (
            "We accept Visa, Mastercard, American Express, PayPal, and Apple Pay. "
            "All transactions are secured with 256-bit SSL encryption."
        ),
        'contact': (
            "You can reach our support team at support@example.com or call 1-800-123-4567 "
            "(Mon-Fri, 9 AM - 6 PM EST)."
        )
    }
    
    return faqs.get(question_type, "I'm here to help! Could you please specify your question?")


# ========== Main Webhook Handler ==========

@functions_framework.http
def webhook(request: Request):
    """
    Main webhook endpoint for Dialogflow CX.
    
    Processes incoming requests and returns fulfillment responses.
    
    Args:
        request: Flask request object with Dialogflow webhook payload
        
    Returns:
        JSON response with fulfillment text and parameters
    """
    try:
        # Parse request
        request_json = request.get_json(silent=True)
        
        if not request_json:
            logger.error("Invalid request: No JSON payload")
            return jsonify({'error': 'Invalid request'}), 400
        
        # Extract Dialogflow parameters
        tag = request_json.get('fulfillmentInfo', {}).get('tag')
        session_info = request_json.get('sessionInfo', {})
        parameters = session_info.get('parameters', {})
        
        logger.info(f"Webhook triggered with tag: {tag}")
        logger.info(f"Parameters: {parameters}")
        
        # Route to appropriate handler
        if tag == 'order_tracking':
            response_text = handle_order_tracking(parameters)
        
        elif tag == 'faq_handler':
            response_text = handle_faq(parameters)
        
        elif tag == 'escalate_human':
            response_text = handle_escalation(parameters)
        
        else:
            response_text = "I'm here to help! You can ask about order status or common questions."
        
        # Build Dialogflow response
        response = {
            'fulfillment_response': {
                'messages': [
                    {
                        'text': {
                            'text': [response_text]
                        }
                    }
                ]
            }
        }
        
        logger.info(f"Sending response: {response_text[:100]}...")
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"Webhook error: {str(e)}", exc_info=True)
        error_response = {
            'fulfillment_response': {
                'messages': [
                    {
                        'text': {
                            'text': ["I encountered an error. Please try again or contact support."]
                        }
                    }
                ]
            }
        }
        return jsonify(error_response), 500


def handle_order_tracking(parameters: Dict[str, Any]) -> str:
    """
    Handle order tracking intent.
    
    Args:
        parameters: Extracted entities from Dialogflow
        
    Returns:
        Order status response string
    """
    order_id = parameters.get('order_id', '').upper()
    
    if not order_id:
        return "Please provide your order ID (e.g., ORD-12345) to track your order."
    
    logger.info(f"Tracking order: {order_id}")
    order_data = get_order_status(order_id)
    
    return format_order_response(order_data, order_id)


def handle_faq(parameters: Dict[str, Any]) -> str:
    """
    Handle FAQ intent.
    
    Args:
        parameters: Extracted entities from Dialogflow
        
    Returns:
        FAQ response string
    """
    question_type = parameters.get('faq_type', 'general')
    
    logger.info(f"FAQ request: {question_type}")
    return get_faq_response(question_type)


def handle_escalation(parameters: Dict[str, Any]) -> str:
    """
    Handle escalation to human agent.
    
    Args:
        parameters: Session parameters
        
    Returns:
        Escalation message
    """
    logger.info("Escalating to human agent")
    return (
        "I'll connect you with a human agent right away. "
        "Please hold for a moment while I transfer you. "
        "Average wait time: 2 minutes."
    )


# ========== Health Check Endpoint ==========

@functions_framework.http
def health(request: Request):
    """Health check endpoint for monitoring."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    })
