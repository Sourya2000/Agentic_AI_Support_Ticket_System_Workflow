#!/usr/bin/env python3
"""
Knowledge Base Ingestion Script
This script loads knowledge base documents into Qdrant with embeddings.
"""

import os
import json
import glob
from pathlib import Path
from typing import List, Dict
import sys


def load_env_file(env_path: str = ".env") -> None:
    """Load simple KEY=VALUE pairs from a .env file into os.environ."""
    if not os.path.isfile(env_path):
        return

    with open(env_path, "r", encoding="utf-8") as env_file:
        for raw_line in env_file:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value

# Try to import required packages
try:
    from openai import OpenAI
    from qdrant_client import QdrantClient
    from qdrant_client.models import Distance, VectorParams, PointStruct
except ImportError:
    print("Error: Required packages not installed.")
    print("Install with: pip install openai qdrant-client")
    sys.exit(1)


class KnowledgeBaseIngestor:
    def __init__(self, openai_api_key: str, qdrant_url: str = "http://localhost:6333"):
        """Initialize the ingestor with API keys and endpoints."""
        self.openai_client = OpenAI(api_key=openai_api_key)
        self.qdrant_client = QdrantClient(url=qdrant_url)
        self.embedding_model = "text-embedding-3-small"
        self.chunk_size = 300  # characters
        self.chunk_overlap = 50  # characters
        
    def chunk_text(self, text: str) -> List[str]:
        """Split text into overlapping chunks."""
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + self.chunk_size
            chunk = text[start:end]
            chunks.append(chunk.strip())
            start += self.chunk_size - self.chunk_overlap
            
        return [c for c in chunks if c]  # Remove empty chunks
    
    def get_embedding(self, text: str) -> List[float]:
        """Get embedding for text using OpenAI."""
        response = self.openai_client.embeddings.create(
            model=self.embedding_model,
            input=text
        )
        return response.data[0].embedding
    
    def load_knowledge_base(self, kb_dir: str) -> List[Dict]:
        """Load all markdown files from knowledge base directory."""
        documents = []
        
        md_files = glob.glob(os.path.join(kb_dir, "*.md"))
        print(f"Found {len(md_files)} markdown files")
        
        for file_path in md_files:
            file_name = os.path.basename(file_path)
            print(f"Loading {file_name}...")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Chunk the content
            chunks = self.chunk_text(content)
            
            for chunk in chunks:
                documents.append({
                    'source': file_name,
                    'content': chunk,
                    'file_path': file_path
                })
        
        return documents
    
    def create_collection(self, collection_name: str = "support_ticket"):
        """Create Qdrant collection for embeddings."""
        try:
            # Check if collection exists
            self.qdrant_client.get_collection(collection_name)
            print(f"Collection '{collection_name}' already exists. Skipping creation.")
        except Exception:
            print(f"Creating collection '{collection_name}'...")
            # Create new collection
            # Vector size for text-embedding-3-small is 1536
            self.qdrant_client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=1536,
                    distance=Distance.COSINE
                )
            )
            print(f"Collection '{collection_name}' created successfully.")
    
    def ingest_documents(self, documents: List[Dict], collection_name: str = "support_ticket"):
        """Ingest documents with embeddings into Qdrant."""
        self.create_collection(collection_name)
        
        points = []
        
        for idx, doc in enumerate(documents):
            print(f"Processing document {idx + 1}/{len(documents)}: {doc['source']}...")
            
            # Get embedding
            embedding = self.get_embedding(doc['content'])
            
            # Create point for Qdrant
            point = PointStruct(
                id=idx,
                vector=embedding,
                payload={
                    'source': doc['source'],
                    'content': doc['content'],
                    'file_path': doc['file_path']
                }
            )
            points.append(point)
        
        # Upload to Qdrant in batches
        batch_size = 10
        for i in range(0, len(points), batch_size):
            batch = points[i:i + batch_size]
            print(f"Uploading batch {i // batch_size + 1}/{(len(points) + batch_size - 1) // batch_size}...")
            self.qdrant_client.upsert(
                collection_name=collection_name,
                points=batch
            )
        
        print(f"Successfully ingested {len(documents)} document chunks into Qdrant!")
        
        # Verify
        collection_info = self.qdrant_client.get_collection(collection_name)
        print(f"Collection info: {collection_info.points_count} points stored")


def main():
    """Main ingestion function."""
    # Load local .env values when present (without overriding shell vars).
    load_env_file()

    # Get configuration from environment
    openai_api_key = os.getenv("OPENAI_API_KEY") or os.getenv("API_KEY")
    if not openai_api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        print("Tip: set OPENAI_API_KEY in your shell or in a local .env file")
        sys.exit(1)
    
    qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
    kb_dir = os.getenv("KB_DIR", "./knowledge-base")
    
    # Verify knowledge base directory exists
    if not os.path.isdir(kb_dir):
        print(f"Error: Knowledge base directory '{kb_dir}' not found")
        sys.exit(1)
    
    print(f"Starting knowledge base ingestion...")
    print(f"  OpenAI API Key: {'***' + openai_api_key[-4:]}")
    print(f"  Qdrant URL: {qdrant_url}")
    print(f"  KB Directory: {kb_dir}")
    print()
    
    try:
        # Initialize ingestor
        ingestor = KnowledgeBaseIngestor(openai_api_key, qdrant_url)
        
        # Load documents
        documents = ingestor.load_knowledge_base(kb_dir)
        print(f"\nLoaded {len(documents)} document chunks")
        
        # Ingest into Qdrant
        print("\nIngesting into Qdrant...")
        ingestor.ingest_documents(documents)
        
        print("\n✓ Knowledge base ingestion complete!")
        
    except Exception as e:
        print(f"Error during ingestion: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
