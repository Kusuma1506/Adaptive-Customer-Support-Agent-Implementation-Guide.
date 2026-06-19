"""Retrieval-Augmented Generation (RAG) Pipeline

This module implements a RAG system using:
- ChromaDB for vector storage
- Sentence Transformers for embeddings
- LangChain for document processing
"""

import os
import logging
from typing import List, Dict, Tuple
from pathlib import Path
import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    TextLoader, 
    DirectoryLoader,
)
from config import config

logger = logging.getLogger(__name__)


class RAGPipeline:
    """Retrieval-Augmented Generation Pipeline"""

    def __init__(self):
        """Initialize RAG pipeline with ChromaDB"""
        self.client = chromadb.PersistentClient(path=config.CHROMA_DB_PATH)
        
        self.collection_name = "cloudsync_kb"
        self.collection = None
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP
        )
        
        # Initialize or get existing collection
        self._init_collection()

    def _init_collection(self):
        """Initialize ChromaDB collection"""
        try:
            # Try to get existing collection
            self.collection = self.client.get_collection(self.collection_name)
            logger.info(f"Loaded existing collection: {self.collection_name}")
        except Exception:
            # Create new collection
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            logger.info(f"Created new collection: {self.collection_name}")

    def ingest_documents(self, docs_path: str) -> Dict:
        """
        Ingest documents from directory into vector store
        
        Args:
            docs_path: Path to directory containing documents
            
        Returns:
            Dictionary with ingestion statistics
        """
        stats = {
            "documents_loaded": 0,
            "chunks_created": 0,
            "errors": []
        }
        
        docs_path = Path(docs_path)
        if not docs_path.exists():
            logger.error(f"Documents directory not found: {docs_path}")
            return stats
        
        # Load markdown files
        md_loader = DirectoryLoader(
            str(docs_path),
            glob="*.md",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"}
        )
        
        try:
            documents = md_loader.load()
            stats["documents_loaded"] += len(documents)
            
            # Process each document
            for doc in documents:
                try:
                    chunks_created = self._process_document(doc)
                    stats["chunks_created"] += chunks_created
                except Exception as e:
                    error_msg = f"Error processing {doc.metadata.get('source', 'unknown')}: {str(e)}"
                    logger.error(error_msg)
                    stats["errors"].append(error_msg)
            
            logger.info(f"Ingested {stats['documents_loaded']} documents, "
                       f"created {stats['chunks_created']} chunks")
            
        except Exception as e:
            logger.error(f"Error loading documents: {str(e)}")
            stats["errors"].append(str(e))
        
        return stats

    def _process_document(self, document) -> int:
        """Process a single document and add to collection"""
        source = document.metadata.get("source", "unknown")
        content = document.page_content
        
        # Split document into chunks
        chunks = self.text_splitter.split_text(content)
        
        # Add chunks to collection
        for i, chunk in enumerate(chunks):
            chunk_id = f"{Path(source).stem}_{i}"
            
            self.collection.add(
                ids=[chunk_id],
                documents=[chunk],
                metadatas=[{
                    "source": source,
                    "chunk_index": i,
                    "chunk_count": len(chunks)
                }]
            )
        
        logger.debug(f"Processed {source}: {len(chunks)} chunks")
        return len(chunks)

    def retrieve(self, query: str, top_k: int = None) -> List[Dict]:
        """
        Retrieve relevant chunks for a query
        
        Args:
            query: User query string
            top_k: Number of results to return (uses config default if None)
            
        Returns:
            List of retrieved documents with metadata
        """
        if top_k is None:
            top_k = config.TOP_K_RETRIEVAL
        
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=top_k
            )
            
            # Format results
            retrieved_docs = []
            if results and results['documents']:
                for i, doc in enumerate(results['documents'][0]):
                    score = results['distances'][0][i] if results['distances'] else 0
                    # Convert distance to similarity (cosine distance to similarity)
                    similarity = 1 - score
                    
                    retrieved_docs.append({
                        "content": doc,
                        "source": results['metadatas'][0][i].get('source', 'unknown'),
                        "chunk_index": results['metadatas'][0][i].get('chunk_index', 0),
                        "similarity": similarity
                    })
            
            logger.debug(f"Retrieved {len(retrieved_docs)} documents for query: {query[:50]}...")
            return retrieved_docs
            
        except Exception as e:
            logger.error(f"Error retrieving documents: {str(e)}")
            return []

    def is_knowledge_base_empty(self) -> bool:
        """Check if knowledge base is empty"""
        try:
            count = self.collection.count()
            return count == 0
        except Exception:
            return True

    def get_collection_stats(self) -> Dict:
        """Get statistics about the collection"""
        try:
            count = self.collection.count()
            return {
                "total_chunks": count,
                "collection_name": self.collection_name,
                "database_path": config.CHROMA_DB_PATH
            }
        except Exception as e:
            logger.error(f"Error getting collection stats: {str(e)}")
            return {}


# Singleton instance
_rag_pipeline = None


def get_rag_pipeline() -> RAGPipeline:
    """Get or create RAG pipeline instance"""
    global _rag_pipeline
    if _rag_pipeline is None:
        _rag_pipeline = RAGPipeline()
    return _rag_pipeline


def initialize_rag_pipeline(docs_path: str = None) -> Dict:
    """
    Initialize RAG pipeline and ingest documents
    
    Args:
        docs_path: Path to documents directory
        
    Returns:
        Dictionary with initialization results
    """
    if docs_path is None:
        docs_path = "./data/kb_documents"
    
    pipeline = get_rag_pipeline()
    
    if pipeline.is_knowledge_base_empty():
        logger.info(f"Knowledge base is empty. Ingesting documents from {docs_path}")
        stats = pipeline.ingest_documents(docs_path)
        logger.info(f"Ingestion complete: {stats}")
        return stats
    else:
        stats = pipeline.get_collection_stats()
        logger.info(f"Knowledge base already populated: {stats}")
        return stats
