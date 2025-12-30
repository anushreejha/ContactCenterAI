#!/bin/bash
# Deploy script for ContactCenterAI Cloud Function
# Usage: ./scripts/deploy.sh

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Deploying ContactCenterAI Webhook...${NC}"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}Error: gcloud CLI not found. Install from https://cloud.google.com/sdk${NC}"
    exit 1
fi

# Get project ID
PROJECT_ID=$(gcloud config get-value project)
if [ -z "$PROJECT_ID" ]; then
    echo -e "${RED}Error: No GCP project set. Run: gcloud config set project YOUR_PROJECT_ID${NC}"
    exit 1
fi

echo -e "${YELLOW}Project ID: ${PROJECT_ID}${NC}"

# Deploy Cloud Function
echo -e "${GREEN}Deploying function...${NC}"
cd cloudfunctions/webhook

gcloud functions deploy dialogflow-webhook \
  --gen2 \
  --runtime=python311 \
  --region=us-central1 \
  --source=. \
  --entry-point=webhook \
  --trigger-http \
  --allow-unauthenticated \
  --set-env-vars PROJECT_ID="${PROJECT_ID}" \
  --memory=256MB \
  --timeout=60s \
  --max-instances=10

# Get function URL
FUNCTION_URL=$(gcloud functions describe dialogflow-webhook --region=us-central1 --gen2 --format='value(serviceConfig.uri)')

echo -e "${GREEN}✅ Deployment complete!${NC}"
echo -e "${YELLOW}Webhook URL: ${FUNCTION_URL}${NC}"
echo -e "${YELLOW}Add this URL to your Dialogflow CX agent webhook configuration.${NC}"
