# NOAVIA Support System — Part 1: AI-Powered Support Ticket Processing

**Status**: Production-ready implementation with RAG, multi-step AI processing, and comprehensive error handling.

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for n8n)
- Python 3.10+ (for knowledge base ingestion)
- OpenAI API key

### Setup in 3 Steps

```bash
# 1. Clone and configure
cd noavia-support-system
export OPENAI_API_KEY='sk-...'
export GOOGLE_SHEETS_ID='your-sheet-id'

# 2. Start services
docker-compose up -d

# 3. Ingest knowledge base
python ingest_kb.py

# Access n8n at http://localhost:5678
```

## What This System Does

1. **Receives** support tickets via webhook (name, email, subject, message, optional PDF)
2. **Validates** input and extracts text from attachments
3. **Classifies** tickets using OpenAI (category, urgency, sentiment, confidence)
4. **Retrieves** relevant knowledge from company KB using RAG (Qdrant + embeddings)
5. **Generates** professional draft responses grounded in company knowledge
6. **Routes** tickets based on urgency (email + logging or logging only)
7. **Stores** everything in Google Sheets with audit trail

## Key Features Delivered

✅ **Multi-Step AI Processing**
- Step 1: Classification with structured JSON validation
- Step 2: Knowledge-augmented draft response generation

✅ **RAG Pipeline** 
- OpenAI text-embedding-3-small (1536 dims)
- Qdrant vector store (5-10 markdowns)
- Top-3 semantic retrieval with source citations

✅ **Smart Routing**
- Critical/High: Email + Google Sheets
- Medium: Email summary + Sheets
- Low: Sheets only
- Low confidence: Always flag for manual review

✅ **Error Handling**
- Multi-layer AI output validation
- Graceful degradation (Qdrant offline → proceeds without KB)
- All errors logged to Google Sheets

✅ **PDF Support**
- Extracts text from attachments
- Appends to ticket for AI analysis
- Logs extraction failures

✅ **Production Deployment**
- Docker Compose (n8n + Qdrant)
- Persistent volumes
- Environment variable configuration (no secrets in code)

## Important Files

- [n8n_workflow_enhanced.json](n8n_workflow_enhanced.json) — Enhanced workflow with all features
- [ingest_kb.py](ingest_kb.py) — Knowledge base ingestion to Qdrant
- [docker-compose.yml](docker-compose.yml) — Services definition
- [IMPLEMENTATION_NOTES.md](IMPLEMENTATION_NOTES.md) — Detailed architecture & design decisions
- [knowledge-base/](knowledge-base/) — Sample company documentation (5-10 markdown files)

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Webhook Intake                           │
│              (POST /support-ticket)                         │
└────────────────────────┬────────────────────────────────────┘
                         ↓
         ┌───────────────────────────────────┐
         │  Validation & Input Processing    │
         │  - Email format check             │
         │  - Required fields check          │
         │  - PDF attachment handling        │
         └────────────────┬────────────────┘
                          ↓
      ┌──────────────────────────────────────────┐
      │    AI Processing (Step 1)                │
      │    OpenAI Classification                 │
      │    → category, urgency, sentiment,       │
      │      confidence, summary                 │
      └────────────┬─────────────────────────────┘
                   ↓
    ┌──────────────────────────────────────────────┐
    │     Know ledgeBase RAG Pipeline              │
    │  1. Create embedding (OpenAI 1536-dim)       │
    │  2. Search Qdrant (cosine similarity)        │
    │  3. Process top-3 results                    │
    │  4. Extract source citations                 │
    └────────────┬─────────────────────────────────┘
                 ↓
      ┌──────────────────────────────────────────┐
      │    AI Processing (Step 2)                │
      │    Generate Draft Response               │
      │    - Match customer sentiment            │
      │    - Ground in KB knowledge              │
      │    - Include source citations            │
      └────────────┬─────────────────────────────┘
                   ↓
         ┌─────────────────────────────────┐
         │  Routing & Storage              │
         │  ┌─────────────────────────┐    │
         │  │ High/Critical Urgency   │    │
         │  │ → Email notification    │    │
         │  │ → Google Sheets         │    │
         │  └─────────────────────────┘    │
         │  ┌─────────────────────────┐    │
         │  │ Low Confidence (< 0.6)  │    │
         │  │ → Flag for review       │    │
         │  │ → Google Sheets         │    │
         │  └─────────────────────────┘    │
         │  ┌─────────────────────────┐    │
         │  │ Error Handling          │    │
         │  │ → Log with details      │    │
         │  │ → Graceful degradation  │    │
         │  └─────────────────────────┘    │
         └─────────────────────────────────┘
                     ↓
         ┌─────────────────────────────────┐
         │  Webhook Response (JSON)        │
         │  { ticket_id, status }          │
         └─────────────────────────────────┘
```

## Google Sheets columns

| Column | Purpose |
|--------|---------|
| A | ticket_id (TCK-timestamp) |
| B | timestamp (ISO 8601) |
| C | name (customer name) |
| D | email |
| E | subject |
| F | category (technical/billing/etc) |
| G | urgency (critical/high/medium/low) |
| H | sentiment (positive/neutral/negative/angry) |
| I | confidence (0.0-1.0) |
| J | ai_summary |
| K | draft_response |
| L | knowledge_sources (JSON array) |
| M | status (normal/needs-manual-review) |
| N | processing_log |

## Testing the Webhook

```bash
curl -X POST http://localhost:n8n:5678/webhook/support-ticket \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "subject": "Payment processing error",
    "message": "I tried to upgrade my plan but got error 500"
  }'
```

Expected response:
```json
{
  "status": "success",
  "ticket_id": "TCK-1712929384000"
}
```

## RAG Implementation Details

See [IMPLEMENTATION_NOTES.md](IMPLEMENTATION_NOTES.md) for:
- **Chunking strategy**: 300-char fixed chunks with 50-char overlap
- **Embedding model**: OpenAI text-embedding-3-small (1536 dims)
- **Retrieval approach**: Top-3 cosine similarity + source citations
- **Low-confidence handling**: Explicit note if retrieval score < threshold

## What Would Improve With More Time

1. **Semantic chunking** — Split on sentence/section boundaries for better context preservation
2. **Reranking** — Add Cohere Rerank or similar for 15-20% accuracy improvement
3. **Cached embeddings** — Reduce API calls and latency
4. **Multi-agent routing** — Separate agents for different domains
5. **Knowledge verification** — Fact-check LLM responses against retrieval
6. **Feedback loop** — Track KB article effectiveness, retrain monthly
7. **Email templates** — Handlebars-based, multi-language support
8. **Rate limiting** — Queue tickets during high volume
9. **Audit trail** — Full GDPR-compliant logging
10. **Dashboard** — Real-time metrics, charts, alerts

See [IMPLEMENTATION_NOTES.md](IMPLEMENTATION_NOTES.md#what-would-improve-with-more-time) for detailed time estimates.

## Part 2 Preparation: German Public Administration

For the on-premise, GDPR-compliant system discussion:

**Key Architecture Points:**
- Fully on-premise stack (no US cloud services)
- German-language embedding model (e.g., `sentence-transformers/multilingual-MiniLM-L6-v2`)
- Qdrant + open-source LLM (Llama 2, Mistral) on German hosting
- Document processing: 2,000 mixed formats with OCR for scanned PDFs
- Semantic chunking for regulatory/procedural docs
- GDPR access control: Role-based retrieval filters

See [IMPLEMENTATION_NOTES.md](IMPLEMENTATION_NOTES.md) for discussion topics.

---

**Developed for NOAVIA AI & Agent Engineer Position** | April 2026
