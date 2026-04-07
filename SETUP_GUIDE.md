# 🚀 Complete Setup Guide - AI Support Ticket Processor

Comprehensive step-by-step instructions to get the system up and running from scratch.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Configuration](#environment-configuration)
3. [Docker Setup](#docker-setup)
4. [Knowledge Base Ingestion](#knowledge-base-ingestion)
5. [n8n Workflow Configuration](#n8n-workflow-configuration)
6. [Integration Setup](#integration-setup)
7. [Testing](#testing)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements

- **Operating System**: Windows, macOS, or Linux
- **Docker**: Version 20.10+ ([Install Docker](https://docs.docker.com/get-docker/))
- **Docker Compose**: Version 2.0+ ([Install Docker Compose](https://docs.docker.com/compose/install/))
- **Python**: Version 3.8+ (for local KB ingestion)
- **Git**: For version control ([Install Git](https://git-scm.com/))
- **Text Editor**: VS Code, Sublime, or similar

### API Keys & Accounts Needed

Before starting, gather the following:

| Item | Source | Why | Required? |
|------|--------|-----|-----------|
| **OpenAI API Key** | https://platform.openai.com/api-keys | Powers AI classification and response generation | ✅ Yes |
| **Google Cloud Project** | https://console.cloud.google.com | For Google Sheets integration | ✅ Yes |
| **Gmail Account** | Gmail | For email alerts (SMTP credentials) | ⚠️ Optional but recommended |
| **Qdrant** | Docker (local) | Vector database (included in docker-compose) | ✅ Auto |

### Directory Structure Check

```
noavia-support-system/
├── n8n_workflow.json           # Workflow definition
├── docker-compose.yml          # Container setup
├── ingest_kb.py               # KB ingestion script
├── requirements.txt            # Python dependencies
├── .env                        # Configuration (YOU CREATE THIS)
├── .env.example               # Template (reference)
├── .gitignore                 # Git exclusions
├── knowledge-base/            # KB documents
│   ├── billing-faq.md
│   ├── technical-setup.md
│   ├── product-features.md
│   ├── support-sla.md
│   ├── troubleshooting.md
│   ├── security-compliance.md
│   └── best-practices.md
└── README.md                  # Overview
```

---

## Environment Configuration

### Step 1: Copy Template to .env

```bash
# Windows PowerShell
Copy-Item .env.example .env

# Or manually copy and edit:
# 1. Open .env.example in text editor
# 2. Save as .env
# 3. Edit values
```

### Step 2: Get OpenAI API Key

**Duration: 5 minutes**

1. Go to https://platform.openai.com/api-keys
2. Sign in with your OpenAI account (or create one)
3. Click **+ Create new secret key**
4. Name it: `n8n-support-processor`
5. Copy the key immediately (you won't see it again)
6. Add to `.env`:

```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Step 3: Configure Google Sheets

**Duration: 15-20 minutes**

#### 3a. Create Google Cloud Project

1. Go to https://console.cloud.google.com/
2. Click project dropdown (top left) → **NEW PROJECT**
3. Name: `NOAVIA Support System`
4. Click **CREATE** (wait ~1 minute)

#### 3b. Enable Required APIs

1. In the search bar, type **Google Sheets API**
2. Click the result → **ENABLE**
3. Search again for **Google Drive API**
4. Click the result → **ENABLE**

#### 3c. Create Service Account

1. Go to **APIs & Services** → **Credentials** (left sidebar)
2. Click **+ CREATE CREDENTIALS** → **Service Account**
3. Fill in:
   - **Service account name**: `n8n-support-bot`
   - Leave Service account ID as auto-generated
   - Click **CREATE AND CONTINUE**
4. **Grant basic Editor role**:
   - Role dropdown → search **Editor**
   - Select **Editor**
   - Click **CONTINUE**
5. Click **DONE**

#### 3d. Create and Download Service Account Key

1. Go to **APIs & Services** → **Credentials**
2. Under **Service Accounts**, click `n8n-support-bot`
3. Click **KEYS** tab
4. Click **ADD KEY** → **Create new key**
5. Select **JSON**
6. Click **CREATE** (JSON file downloads)
7. **Move file to project root** and rename to `google-credentials.json`
8. **DO NOT** commit to git (already in .gitignore)

#### 3e. Create Google Sheet

1. Go to https://sheets.google.com
2. Click **+ BLANK** to create new sheet
3. Name it: `Support Tickets`
4. In cell A1, add headers (one per column):
   ```
   A1: Ticket ID
   B1: Timestamp
   C1: Name
   D1: Email
   E1: Subject
   F1: Category
   G1: Urgency
   H1: Sentiment
   I1: Confidence
   J1: AI Summary
   K1: Draft Response
   L1: Knowledge Sources
   M1: Status
   ```
5. Copy the **Sheet ID** from URL:
   ```
   https://docs.google.com/spreadsheets/d/[COPY-THIS-ID]/edit
   ```

#### 3f. Share Google Sheet with Service Account

1. Open `google-credentials.json` in text editor
2. Copy the value of `"client_email"` (looks like: `name@project.iam.gserviceaccount.com`)
3. Go back to your Google Sheet
4. Click **Share** (top right)
5. Paste the service account email
6. Select **Editor**
7. Click **Share**

#### 3g. Update .env File

Edit `.env` and add:

```env
# Google Sheets Configuration
GOOGLE_SHEET_ID=1A2BCD3EFG4HIJ5K6L7MN8OPQR9ST0UV1W2XYZ3
GOOGLE_SHEETS_KEYFILE=./google-credentials.json
```

**Replace with YOUR actual Sheet ID!**

### Step 4: Email Configuration (Optional but Recommended)

For sending alert emails to support team.

#### Using Gmail with App Password

1. Go to https://myaccount.google.com/security
2. Enable **2-Step Verification** if not already enabled
3. Go to https://myaccount.google.com/apppasswords
4. Select **Mail** and **Windows Computer** (or your device)
5. Click **GENERATE**
6. Copy the 16-character password
7. Update `.env`:

```env
# Email Configuration
EMAIL_SMTP_HOST=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_SMTP_USER=your-email@gmail.com
EMAIL_SMTP_PASSWORD=xxxx xxxx xxxx xxxx
EMAIL_FROM=alerts@company.com
SUPPORT_ESCALATION_EMAIL=your-email@gmail.com
```

**Note**: Use the 16-character app password, not your regular Gmail password.

### Step 5: Other Configuration

Update remaining `.env` variables:

```env
# n8n Configuration
N8N_HOST=0.0.0.0
N8N_PORT=5678
WEBHOOK_TUNNEL_URL=http://localhost:5678/
TIMEZONE=UTC

# Qdrant Configuration
QDRANT_URL=http://qdrant:6333
QDRANT_API_KEY=your-secure-api-key

# Knowledge Base Settings
KB_DIR=./knowledge-base
KNOWLEDGE_COLLECTION_NAME=support_kb
CHUNKING_SIZE=300
CHUNKING_OVERLAP=50

# Routing Configuration
CONFIDENCE_THRESHOLD=0.6
RETRIEVAL_SCORE_THRESHOLD=0.6
```

### Final .env Check

Your `.env` file should now have (at minimum):

```bash
✓ OPENAI_API_KEY=sk-proj-...
✓ GOOGLE_SHEET_ID=1ABC...
✓ GOOGLE_SHEETS_KEYFILE=./google-credentials.json
✓ EMAIL_SMTP_USER=your-email@gmail.com
✓ EMAIL_SMTP_PASSWORD=xxxx xxxx xxxx xxxx
✓ QDRANT_API_KEY=your-secure-key
```

---

## Docker Setup

### Step 1: Verify Docker Installation

```bash
# Check Docker
docker --version

# Check Docker Compose
docker-compose --version

# Both should display version numbers
```

### Step 2: Start Services

```bash
# Navigate to project directory
cd path/to/noavia-support-system

# Start all services
docker-compose up -d

# Check status
docker-compose ps
```

Expected output:
```
NAME                 STATUS           PORTS
n8n                  Up 2 minutes     0.0.0.0:5678->5678/tcp
qdrant               Up 2 minutes     0.0.0.0:6333->6333/tcp,0.0.0.0:6334->6334/tcp
```

### Step 3: Verify Services are Healthy

```bash
# Check n8n
curl http://localhost:5678
# Should return HTML (n8n dashboard)

# Check Qdrant
curl http://localhost:6333/health
# Should return: {"status":"ok"}
```

### Step 4: View Logs (if needed)

```bash
# See n8n logs
docker-compose logs n8n

# See Qdrant logs
docker-compose logs qdrant

# Follow logs in real-time
docker-compose logs -f n8n
```

---

## Knowledge Base Ingestion

This loads your company documentation into Qdrant for semantic search.

### Step 1: Install Python Dependencies

```bash
# Navigate to project directory
cd path/to/noavia-support-system

# Activate virtual environment (if you have one)
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### Step 2: Run Knowledge Base Ingestion

```bash
# Set OpenAI API key in environment
# Windows PowerShell:
$env:OPENAI_API_KEY = "sk-proj-your-key-here"

# macOS/Linux bash:
export OPENAI_API_KEY="sk-proj-your-key-here"

# Run ingestion script
python ingest_kb.py
```

**Expected output:**
```
Starting knowledge base ingestion...
  OpenAI API Key: ***key-last-4-digits
  Qdrant URL: http://localhost:6333
  KB Directory: ./knowledge-base

Found 7 markdown files
Loading billing-faq.md...
Processing document 1/50: billing-faq.md...
...
Successfully ingested 50 document chunks into Qdrant!
Collection info: 50 points stored
✓ Knowledge base ingestion complete!
```

### Step 3: Verify Ingestion

```bash
# Check Qdrant has documents
curl http://localhost:6333/collections/support_kb

# Should show: "points_count": 50 (approximate)
```

---

## n8n Workflow Configuration

### Step 1: Access n8n Dashboard

1. Open browser: http://localhost:5678
2. Create account (first time setup)
   - Email: your-email@example.com
   - Password: strong-password
   - Click **Sign me up**

### Step 2: Import Workflow

1. Click **NEW WORKFLOW**
2. Click three dots menu (top left) → **Import from file**
3. Select **n8n_workflow.json** from your project folder
4. Click **Import**

### Step 3: Configure Credentials

#### 3a. OpenAI API Key

1. Click **Credentials** (bottom left)
2. Click **+ Add** 
3. Search: **OpenAI**
4. Select **OpenAI API**
5. Credential name: `OpenAI`
6. API Key: Paste your `OPENAI_API_KEY`
7. Click **Save**

#### 3b. Google Sheets

1. Click **Credentials** → **+ Add**
2. Search: **Google Sheets**
3. Select **Google Sheets**
4. Credential name: `Google Sheets`
5. Authentication method: **Service Account (via JSON credential file)**
6. Click **Select File** → Choose `google-credentials.json`
7. Click **Save**

#### 3c. Email (Optional)

1. Click **Credentials** → **+ Add**
2. Search: **Gmail** or **SMTP**
3. Select **Gmail** or **SMTP**
4. Fill in your email credentials
5. Click **Save**

### Step 4: Update Workflow Node Credentials

1. Open imported workflow
2. Find each node that needs credentials:
   - **AI Classification** node → Select OpenAI credential
   - **AI Draft Response** node → Select OpenAI credential
   - **Google Sheets Log** node → Select Google Sheets credential
   - **Send Alert Email** node → Select Email credential

3. Update **Google Sheets Log** node:
   - Sheet ID: Paste your actual Sheet ID
   - Make sure columns match (Ticket ID, Timestamp, etc.)

### Step 5: Activate Workflow

1. Click **Activate** button (top right)
2. Status should show **Active** (green)
3. You'll see a webhook URL:
   ```
   https://your-domain/webhook/support-ticket
   ```
   (or locally: `http://localhost:5678/webhook/support-ticket`)

---

## Integration Setup

### Connect Your Support Form

Point your support form to the webhook:

```
POST http://localhost:5678/webhook/support-ticket
```

**Expected payload:**

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "subject": "Billing Issue",
  "message": "I was charged twice this month",
  "file": {
    "url": "https://example.com/document.pdf"
  }
}
```

**Response:**

```json
{
  "ticketId": "1712425600000-a7k3f9",
  "status": "processed",
  "urgency": "medium",
  "confidence": 0.92
}
```

### Verify Google Sheets Connection

1. Send a test ticket (see Testing section)
2. Check your Google Sheet
3. New row should appear with all ticket data

---

## Testing

### Test 1: Manual Webhook Test

```bash
# Using curl
curl -X POST http://localhost:5678/webhook/support-ticket \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "subject": "Test Ticket",
    "message": "This is a test message"
  }'
```

**Expected response:**
```json
{
  "ticketId": "1712425600000-abc123",
  "status": "processed",
  "urgency": "medium",
  "confidence": 0.85
}
```

### Test 2: Check n8n Execution

1. In n8n, go to **Executions** tab
2. Click the latest execution
3. Verify all nodes completed (green checkmarks)
4. Check data flow through each node

### Test 3: Verify Google Sheets

1. Open your Google Sheet
2. New row should appear with:
   - Ticket ID, Timestamp, Name, Email
   - Category, Urgency, Sentiment, Confidence
   - AI Summary, Draft Response
   - Status: "processed" or "needs-manual-review"

### Test 4: Check Email Alert (if configured)

1. Send a "critical" ticket:
   ```bash
   curl -X POST http://localhost:5678/webhook/support-ticket \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Critical User",
       "email": "critical@example.com",
       "subject": "System Down",
       "message": "The entire system is unavailable!"
     }'
   ```

2. Check your email inbox
3. Should receive alert email from `alerts@company.com`

### Test 5: PDF Attachment (Optional)

1. Create a test PDF file
2. Upload it to a publicly accessible URL
3. Send ticket with file URL:

```bash
curl -X POST http://localhost:5678/webhook/support-ticket \
  -H "Content-Type: application/json" \
  -d '{
    "name": "PDF User",
    "email": "pdf@example.com",
    "subject": "Issue with PDF",
    "message": "See attached document",
    "file": {
      "url": "https://example.com/test.pdf"
    }
  }'
```

4. Check n8n logs for PDF extraction
5. Verify extracted text appears in Google Sheet

---

## Troubleshooting

### Docker Issues

#### Services won't start

```bash
# Check if ports are already in use
# Windows:
netstat -ano | findstr :5678
netstat -ano | findstr :6333

# macOS/Linux:
lsof -i :5678
lsof -i :6333

# Solution: Kill process or change docker-compose ports
```

#### Docker logs show errors

```bash
# View detailed logs
docker-compose logs n8n
docker-compose logs qdrant

# Stop and restart
docker-compose restart

# Full reset (warning: deletes data)
docker-compose down -v
docker-compose up -d
```

### n8n Issues

#### Can't connect to Qdrant

1. Verify Qdrant is running:
   ```bash
   curl http://localhost:6333/health
   ```
2. Check n8n logs:
   ```bash
   docker-compose logs n8n | grep -i qdrant
   ```
3. Verify URL in Qdrant Search node (default: `http://qdrant:6333`)

#### OpenAI API errors

| Error | Solution |
|-------|----------|
| "Invalid API key" | Verify key in credentials, check it's not expired |
| "Rate limit exceeded" | Wait a minute, upgrade OpenAI plan, batch requests |
| "Model not found" | Verify gpt-4o-mini is available in your region |
| "Insufficient quota" | Check OpenAI billing: https://platform.openai.com/account/billing |

#### Google Sheets not receiving data

1. Verify Sheet ID is correct (copy from URL)
2. Confirm service account email has Editor access
3. Check all column names match exactly:
   ```
   "Ticket ID", "Timestamp", "Name", "Email", "Subject",
   "Category", "Urgency", "Sentiment", "Confidence",
   "AI Summary", "Draft Response", "Knowledge Sources", "Status"
   ```
4. Check n8n credential is selected in Google Sheets node
5. Look at n8n logs:
   ```bash
   docker-compose logs n8n | grep -i "sheet\|google"
   ```

### Knowledge Base Issues

#### Ingestion script fails

```bash
# Check API key is set
echo $OPENAI_API_KEY  # Should show your key

# Check knowledge-base directory exists and has files
ls -la knowledge-base/

# Run with verbose output
python ingest_kb.py

# If Qdrant connection fails, ensure it's running:
curl http://localhost:6333/health
```

#### No results from Qdrant Search

1. Verify ingestion completed successfully
2. Check collection exists:
   ```bash
   curl http://localhost:6333/collections/support_kb
   ```
3. If collection is empty, re-run ingest_kb.py
4. Verify similarity threshold in Qdrant Search node (default: 0.6)

### Webhook Issues

#### Getting "Not Found" when calling webhook

1. Verify workflow is **Activated** (green button)
2. Check exact webhook URL in n8n
3. For local testing, use: `http://localhost:5678/webhook/support-ticket`
4. For production, may need ngrok tunnel:
   ```bash
   ngrok http 5678
   # Use provided https://xxxx.ngrok.io/webhook/support-ticket
   ```

#### Webhook returns 500 error

1. Check n8n execution logs for which node failed
2. Look for credential issues
3. Verify node configuration (especially Google Sheets Sheet ID)
4. Check system resources (disk, memory):
   ```bash
   docker stats
   ```

---

## Monitoring & Maintenance

### Daily Checks

```bash
# Services running?
docker-compose ps

# Any errors in logs?
docker-compose logs --tail=50 n8n
docker-compose logs --tail=50 qdrant
```

### Weekly Maintenance

```bash
# Review execution history in n8n
# Check for failed workflows
# Verify Google Sheet is being populated

# Clean old logs (optional)
docker exec n8n rm -f /home/node/.n8n/workflows.db.backup
```

### Monthly Tasks

- Review and classify any "needs-manual-review" tickets
- Check API usage and costs:
  - OpenAI: https://platform.openai.com/account/billing/usage
  - Google: https://console.cloud.google.com/billing
- Rotate service account keys (recommended quarterly)
- Update n8n and Docker images:
  ```bash
  docker-compose pull
  docker-compose up -d
  ```

### Backup Strategy

```bash
# Backup Qdrant data
docker exec qdrant tar czf /qdrant/storage/backup.tar.gz /qdrant/storage

# Backup n8n database
docker exec n8n cp /home/node/.n8n/workflows.db ./backup/

# Backup Google Sheet (manual)
# File → Download → PDF or Excel
```

---

## Next Steps

1. ✅ Complete all setup steps above
2. ✅ Run Test 1-5 to verify everything works
3. ✅ Connect your actual support form
4. ✅ Monitor first week of tickets
5. 📖 Read README.md for architecture details
6. 🔍 Review IMPLEMENTATION_SUMMARY.md for feature overview

---

## Support & Documentation

- **n8n Docs**: https://docs.n8n.io
- **Qdrant Docs**: https://qdrant.tech/documentation/
- **OpenAI Docs**: https://platform.openai.com/docs
- **Google Sheets API**: https://developers.google.com/sheets
- **Docker Docs**: https://docs.docker.com

---

## Quick Reference

### Common Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f n8n

# Run knowledge base ingestion
python ingest_kb.py

# Test webhook
curl -X POST http://localhost:5678/webhook/support-ticket \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@test.com","subject":"Test","message":"Test"}'

# Access n8n
open http://localhost:5678  # macOS
start http://localhost:5678  # Windows
xdg-open http://localhost:5678  # Linux
```

### File Locations (Inside Docker)

```
n8n workflows: /home/node/.n8n
Qdrant data: /qdrant/storage
n8n database: /home/node/.n8n/workflows.db
```

### Port Mappings

```
n8n Web UI:     http://localhost:5678
Qdrant API:     http://localhost:6333
Qdrant Admin:   http://localhost:6334
Support Webhook: http://localhost:5678/webhook/support-ticket
```

---

**Last Updated**: April 2026
**Status**: ✅ Ready for Production
