"""
Vector Database - ChromaDB wrapper
"""

import chromadb
import os
from typing import List, Dict, Any
from pathlib import Path
from core.config import Config


class VectorDatabase:
    """Wrapper for ChromaDB vector database"""
    
    def __init__(self, config: Config):
        """Initialize vector database"""
        self.config = config
        self.db_path = config.get("database_path", "./data/chroma_db")
        
        # Create directory if not exists
        Path(self.db_path).mkdir(parents=True, exist_ok=True)
        
        # Initialize ChromaDB
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(
            name="knowledge_base",
            metadata={"hnsw:space": "cosine"}
        )
    
    def add_documents(self, documents: List[str], source: str = "unknown") -> bool:
        """Add documents to database"""
        try:
            if not documents:
                return False
            
            # Add documents with metadata
            for i, doc in enumerate(documents):
                self.collection.add(
                    ids=[f"{source}_{i}"],
                    documents=[doc],
                    metadatas=[{"source": source}]
                )
            
            return True
        
        except Exception as e:
            print(f"Error adding documents: {str(e)}")
            return False
    
    def search(self, query: str, limit: int = 3) -> List[str]:
        """Search for similar documents"""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=limit
            )
            
            if results and results['documents']:
                return results['documents'][0]
            
            return []
        
        except Exception as e:
            print(f"Error searching: {str(e)}")
            return []
    
    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        try:
            count = self.collection.count()
            return {
                "total_documents": count,
                "database_path": self.db_path
            }
        except:
            return {"total_documents": 0, "database_path": self.db_path}
    
    def clear(self) -> bool:
        """Clear database"""
        try:
            self.client.delete_collection(name="knowledge_base")
            self.collection = self.client.get_or_create_collection(
                name="knowledge_base",
                metadata={"hnsw:space": "cosine"}
            )
            return True
        except Exception as e:
            print(f"Error clearing database: {str(e)}")
            return False
