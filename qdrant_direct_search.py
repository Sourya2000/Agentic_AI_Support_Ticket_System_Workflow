
import os
from qdrant_client import QdrantClient
from openai import OpenAI

# Load .env if present
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from current directory if it exists
env_path = Path('.') / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=env_path)


# --- CONFIGURATION ---
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION", "support_ticket")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not set in environment or .env file.")

# The test message you want to search for
query_text = (
    "I am seeing incomplete or missing data in my results. "
    "Could this be a field mapping issue or schema mismatch? "
    "How do I check for null values in required fields and use the field mapping UI to map columns explicitly?"
)

# --- GET EMBEDDING ---
openai_client = OpenAI(api_key=OPENAI_API_KEY)
embedding_model = "text-embedding-3-small"
embedding = openai_client.embeddings.create(
    model=embedding_model,
    input=query_text
).data[0].embedding

# --- QDRANT SEARCH ---
client = QdrantClient(url=QDRANT_URL)
search_results = client.search_points(
    collection_name=COLLECTION_NAME,
    query_vector=embedding,
    limit=10  # Adjust as needed
)

print("Top Qdrant search results for your query:")
for idx, result in enumerate(search_results, 1):
    payload = result.payload
    print(f"\nResult {idx}:")
    print(f"  Source: {payload.get('source')}")
    print(f"  File Path: {payload.get('file_path')}")
    print(f"  Content: {payload.get('content')[:200]}...")  # Print first 200 chars
    print(f"  Score: {result.score:.4f}")