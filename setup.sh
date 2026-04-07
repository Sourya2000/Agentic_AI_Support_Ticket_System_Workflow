#!/bin/bash

# Quick Start Setup Script for AI Support Ticket Processor
# This script sets up the environment and starts the services

set -e

echo "================================"
echo "AI Support Ticket Processor"
echo "Quick Start Setup"
echo "================================"
echo ""

# Check for Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "   https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "   https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✓ Docker and Docker Compose found"
echo ""

# Check for .env file
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env
    echo "✓ Created .env file"
    echo ""
    echo "📝 Please edit .env with your configuration:"
    echo "   - OPENAI_API_KEY (required)"
    echo "   - GOOGLE_APPLICATION_CREDENTIALS_JSON (required for Google Sheets)"
    echo "   - EMAIL_SMTP_USER, EMAIL_SMTP_PASSWORD (for alerts)"
    echo ""
    read -p "Continue after updating .env? (y/n) " -n 1 -r
    echo ""
    if [ ! "$REPLY" = "y" ]; then
        exit 1
    fi
else
    echo "✓ Found existing .env file"
fi

# Check if .env has required keys
if ! grep -q "OPENAI_API_KEY=" .env; then
    echo "❌ OPENAI_API_KEY not set in .env"
    exit 1
fi

echo ""
echo "Starting services with Docker Compose..."
echo ""

# Start services
docker-compose down -v 2>/dev/null || true
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check n8n
echo ""
echo "Checking n8n health..."
if curl -s http://localhost:5678 > /dev/null; then
    echo "✓ n8n is ready at http://localhost:5678"
else
    echo "⚠️  n8n may still be starting, check http://localhost:5678"
fi

# Check Qdrant
echo ""
echo "Checking Qdrant health..."
if curl -s http://localhost:6333/health > /dev/null; then
    echo "✓ Qdrant is ready at http://localhost:6333"
else
    echo "⚠️  Qdrant may still be starting, check http://localhost:6333/health"
fi

echo ""
echo "================================"
echo "Service Status"
echo "================================"
docker-compose ps

echo ""
echo "================================"
echo "Next Steps"
echo "================================"
echo ""
echo "1. Open n8n at http://localhost:5678"
echo "2. Create account and login"
echo "3. Import the workflow (n8n_workflow.json):"
echo "   - Create a new workflow"
echo "   - Import → Database → Load from file JSON"
echo "   - Select n8n_workflow.json"
echo ""
echo "4. Configure credentials in n8n:"
echo "   - OpenAI API key"
echo "   - Google Sheets"
echo "   - Email (optional)"
echo ""
echo "5. Ingest knowledge base:"
echo "   - For local: pip install openai qdrant-client"
echo "              export OPENAI_API_KEY=<your-key>"
echo "              python ingest_kb.py"
echo ""
echo "   - Or in Docker: docker-compose exec -T n8n python /data/ingest_kb.py"
echo ""
echo "6. Test webhook:"
echo "   - curl -X POST http://localhost:5678/webhook/support-ticket \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"name\":\"Test\",\"email\":\"test@example.com\",\"subject\":\"Test\",\"message\":\"Test message\"}'"
echo ""
echo "📖 For more details, see README.md"
echo ""
