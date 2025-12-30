# 🤖 ContactCenterAI

Customer service chatbot built with Dialogflow CX and Cloud Functions. Handles order tracking and FAQs with webhook fulfillment.

## Features

- Intent recognition and entity extraction
- Order tracking via webhook
- FAQ responses (shipping, returns, refunds)
- Multi-turn conversation flows
- Error handling and logging

## Architecture

```
User → Dialogflow CX → Cloud Functions Webhook → Backend API
                    ↓
            Dynamic Responses
```

## Tech Stack

- **Dialogflow CX** - Intent matching, NLU
- **Cloud Functions** - Python webhook
- **pytest** - Testing

## Setup

1. Clone the repo:
```
git clone https://github.com/anushreejha/ContactCenterAI.git
cd ContactCenterAI
```
2. Configure GCP:
```
export PROJECT_ID="your-project-id"
gcloud config set project $PROJECT_ID
gcloud services enable dialogflow.googleapis.com cloudfunctions.googleapis.com
```

3. Deploy webhook:
```
cd cloudfunctions/webhook
gcloud functions deploy dialogflow-webhook --runtime python311 --trigger-http --entry-point webhook --region us-central1
```

4. Import intents from dialogflow/intents/ using the Dialogflow CX console at dialogflow.```cloud.google.com/cx```

## Project Structure

```
ContactCenterAI/
├── cloudfunctions/
│   └── webhook/
│       ├── main.py
│       └── requirements.txt
├── dialogflow/
│   ├── intents/
│   │   ├── order_tracking.json
│   │   ├── faq_shipping.json
│   │   ├── faq_returns.json
│   │   └── welcome.json
│   └── entities/
│       └── order_id.json
├── tests/
│   ├── __init__.py
│   ├── test_webhook.py
│   └── fixtures/
│       └── sample_requests.json
├── docs/
│   └── ARCHITECTURE.md
├── scripts/
│   ├── deploy.sh
│   └── setup_gcp.sh
├── .gcloudignore
├── .gitignore
├── README.md
└── requirements-dev.txt
```

## Usage

Order Tracking:
User: What's my order status?
Bot: Please provide your order ID.
User: ORD-12345
Bot: Your order is in transit. Expected delivery: Dec 28, 2025.

FAQ:
User: What's your return policy?
Bot: We offer 30-day returns for unused items.

## Testing

Run tests:
```
pytest tests/test_webhook.py -v
```

Test locally:
```
cd cloudfunctions/webhook
functions-framework --target=webhook --debug
```

## Configuration

Local dev environment variables (.env):
```
PROJECT_ID=your-project-id
ORDER_API_URL=<api-link>
```
