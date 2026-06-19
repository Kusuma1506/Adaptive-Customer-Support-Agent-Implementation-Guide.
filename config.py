"""Configuration management for the support agent"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Ollama Configuration
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    LLM_MODEL = os.getenv("LLM_MODEL", "mistral")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
    
    # ChromaDB Configuration
    CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./data/chromadb")
    
    # RAG Configuration
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "800"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "100"))
    
    # Application Configuration
    ESCALATION_THRESHOLD = float(os.getenv("ESCALATION_THRESHOLD", "0.5"))
    MAX_CONTEXT_TOKENS = int(os.getenv("MAX_CONTEXT_TOKENS", "4000"))
    TOP_K_RETRIEVAL = int(os.getenv("TOP_K_RETRIEVAL", "5"))
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Personas
    PERSONAS = {
        "technical_expert": {
            "keywords": ["api", "error", "log", "debug", "stack trace", "configuration", "integration", "authentication", "endpoint", "webhook"],
            "tone": "technical"
        },
        "frustrated_user": {
            "keywords": ["frustrated", "not working", "broken", "help", "please", "urgent", "critical", "asap", "angry", "disappointed"],
            "tone": "empathetic"
        },
        "business_executive": {
            "keywords": ["impact", "business", "operations", "timeline", "resolution", "uptime", "revenue", "productivity", "cost", "risk"],
            "tone": "concise"
        }
    }

config = Config()
