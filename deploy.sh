#!/bin/bash

echo "🚀 Deploying Food Vision Analyzer to Netlify..."

# Check if netlify CLI is installed
if ! command -v netlify &> /dev/null; then
    echo "❌ Netlify CLI not found. Installing..."
    npm install -g netlify-cli
fi

# Login to Netlify (this will open browser)
echo "🔐 Please login to Netlify in your browser..."
netlify login

# Deploy to production
echo "📤 Deploying to production..."
netlify deploy --prod --dir=. --message "Deploy Food Vision Analyzer App"

echo "✅ Deployment complete!"
echo "🌐 Your app should now be live on Netlify!"