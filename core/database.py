"""
Vector Database - ChromaDB integration for semantic search
"""

from typing import List, Dict, Optional
import chromadb
from chromadb.config import Settings
from core.config import Config
import os


class VectorDatabase:
    """Vector database for storing and searching documents"""
    
    def __init__(self, config: Config):
        """Initialize vector database"""
        self.config = config
        self.db_path = config.get("database_path", "./data/chroma_db")
        self.collection_name = "knowledge_base"
        
        # Create directory if it doesn't exist
        os.makedirs(self.db_path, exist_ok=True)
        
        # Initialize ChromaDB
        settings = Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=self.db_path,
            anonymized_telemetry=False,
        )
        
        self.client = chromadb.Client(settings)
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        
        self.doc_count = 0
        self._load_doc_count()
    
    def _load_doc_count(self) -> None:
        """Load document count from collection"""
        try:
            self.doc_count = self.collection.count()
        except:
            self.doc_count = 0
    
    def add_documents(self, documents: List[str], source_url: str = "") -> bool:
        """Add documents to the database"""
        try:
            if not documents:
                return False
            
            # Prepare documents with IDs and metadata
            ids = [f"doc_{self.doc_count + i}" for i in range(len(documents))]
            metadatas = [
                {
                    "source": source_url,
                    "chunk_index": i,
                    "timestamp": str(__import__('datetime').datetime.now())
                }
                for i in range(len(documents))
            ]
            
            # Add to collection
            self.collection.add(
                ids=ids,
                documents=documents,
                metadatas=metadatas
            )
            
            # Update count
            self.doc_count += len(documents)
            
            print(f"✅ Added {len(documents)} documents from {source_url}")
            return True
        
        except Exception as e:
            print(f"❌ Error adding documents: {str(e)}")
            return False
    
    def search(self, query: str, limit: int = 3) -> List[str]:
        """Search for relevant documents"""
        try:
            if not query.strip():
                return []
            
            results = self.collection.query(
                query_texts=[query],
                n_results=limit,
                where_document={"$contains": query[:10]} if len(query) > 10 else None
            )
            
            if results and results["documents"]:
                return results["documents"][0]
            
            return []
        
        except Exception as e:
            print(f"❌ Error searching: {str(e)}")
            return []
    
    def search_with_scores(self, query: str, limit: int = 3) -> List[tuple]:
        """Search with relevance scores"""
        try:
            if not query.strip():
                return []
            
            results = self.collection.query(
                query_texts=[query],
                n_results=limit,
                include=["documents", "distances"]
            )
            
            if results and results["documents"]:
                docs = results["documents"][0]
                distances = results["distances"][0]
                
                # Convert distances to similarity scores (cosine distance to similarity)
                scores = [1 - d for d in distances]
                
                return list(zip(docs, scores))
            
            return []
        
        except Exception as e:
            print(f"❌ Error searching with scores: {str(e)}")
            return []
    
    def get_stats(self) -> Dict:
        """Get database statistics"""
        try:
            return {
                "total_documents": self.doc_count,
                "collection_name": self.collection_name,
                "database_path": self.db_path,
                "storage_type": "ChromaDB (DuckDB)"
            }
        except Exception as e:
            return {"error": str(e)}
    
    def clear(self) -> bool:
        """Clear all documents from database"""
        try:
            # Delete collection and recreate it
            self.client.delete_collection(name=self.collection_name)
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            self.doc_count = 0
            print("✅ Database cleared")
            return True
        
        except Exception as e:
            print(f"❌ Error clearing database: {str(e)}")
            return False
    
    def delete_document(self, doc_id: str) -> bool:
        """Delete a specific document"""
        try:
            self.collection.delete(ids=[doc_id])
            self.doc_count = max(0, self.doc_count - 1)
            return True
        except Exception as e:
            print(f"❌ Error deleting document: {str(e)}")
            return False
    
    def update_document(self, doc_id: str, new_content: str, metadata: Dict = None) -> bool:
        """Update a document"""
        try:
            self.collection.update(
                ids=[doc_id],
                documents=[new_content],
                metadatas=[metadata] if metadata else None
            )
            return True
        except Exception as e:
            print(f"❌ Error updating document: {str(e)}")
            return False
    
    def persist(self) -> None:
        """Persist database to disk"""
        try:
            self.client.persist()
            print("✅ Database persisted")
        except Exception as e:
            print(f"❌ Error persisting database: {str(e)}")
    
    def get_all_documents(self) -> List[Dict]:
        """Get all documents from database"""
        try:
            # Get all documents from collection
            results = self.collection.get(
                include=["documents", "metadatas"]
            )
            
            documents = []
            if results["documents"]:
                for doc, metadata in zip(results["documents"], results["metadatas"]):
                    documents.append({
                        "content": doc,
                        "metadata": metadata
                    })
            
            return documents
        
        except Exception as e:
            print(f"❌ Error retrieving documents: {str(e)}")
            return []
