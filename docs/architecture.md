# Architecture

## Flow Diagram
User → Dialogflow CX (Intent Recognition) → Cloud Function Webhook → (Mock) Backend API

## Components

### Dialogflow CX
- Intent matching & NLU
- Entity extraction (order IDs, dates)
- Session management

### Cloud Function Webhook
- Python 3.11 runtime
- Handles fulfillment requests
- Routes to appropriate handler
- Returns dynamic responses

### Backend Integration (Mock)
- Simulates order database
- In production: REST API calls to inventory system

## Scalability
- Cloud Functions auto-scale (0 to N instances)
- Stateless design (session in Dialogflow)
- Max 10 concurrent instances configured
