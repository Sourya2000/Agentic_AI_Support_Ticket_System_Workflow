#!/usr/bin/env python3
import os
import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

openai = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
qdrant_url = os.getenv('QDRANT_URL', 'http://localhost:6333')

test_query = 'Production checkout failing for all customers HTTP 500 cannot complete payment critical outage'
print(f'Testing retrieval for query: "{test_query}"\n')

# Get embedding
embedding = openai.embeddings.create(
    model='text-embedding-3-small',
    input=test_query
).data[0].embedding

print(f'Embedding dimension: {len(embedding)}\n')

# Search Qdrant via HTTP
search_url = f'{qdrant_url}/collections/support_ticket/points/search'
headers = {
    'Content-Type': 'application/json',
    'api-key': os.getenv('QDRANT_API_KEY', '')
}
payload = {
    'vector': embedding,
    'limit': 5,
    'with_payload': True
}

response = requests.post(search_url, json=payload, headers=headers)
data = response.json()

if 'result' in data:
    results = data['result']
    print('Top 5 retrieval matches:\n')
    for i, result in enumerate(results, 1):
        score = result.get('score', 0)
        source = result.get('payload', {}).get('source', 'Unknown')
        content = result.get('payload', {}).get('content', '')[:120]
        print(f'{i}. Score: {score:.4f} | Source: {source}')
        print(f'   Content: {content}...\n')
else:
    print(f'Error: {data}')
