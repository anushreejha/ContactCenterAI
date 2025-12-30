#!/bin/bash
# Initial GCP setup for ContactCenterAI
# Run once to enable APIs and set up permissions

set -e

echo "🔧 Setting up Google Cloud Project for ContactCenterAI..."

# Enable required APIs
echo "Enabling APIs..."
gcloud services enable dialogflow.googleapis.com
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable logging.googleapis.com

echo "✅ APIs enabled successfully!"

# Create service account (optional, for production)
echo "Creating service account..."
gcloud iam service-accounts create contactcenterai-sa \
  --display-name="ContactCenterAI Service Account" \
  --description="Service account for ContactCenterAI webhook" || echo "Service account already exists"

PROJECT_ID=$(gcloud config get-value project)
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:contactcenterai-sa@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/dialogflow.client" || true

echo "✅ Setup complete!"
echo "Next steps:"
echo "1. Run: ./scripts/deploy.sh"
echo "2. Configure Dialogflow agent"
echo "3. Import intents from dialogflow/intents/"
