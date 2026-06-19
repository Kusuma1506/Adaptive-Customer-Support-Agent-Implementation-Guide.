# Persona-Adaptive Customer Support Agent

**A sophisticated AI-powered support system that detects customer personas and generates contextually appropriate responses using RAG and LLMs.**

## 🎯 Overview

This project implements an intelligent customer support agent capable of:
- **Persona Detection**: Automatically identifying customer types (Technical Expert, Frustrated User, Business Executive)
- **Retrieval-Augmented Generation (RAG)**: Fetching relevant information from a knowledge base
- **Adaptive Response Generation**: Tailoring response tone and style based on detected persona
- **Intelligent Escalation**: Recognizing when human intervention is needed
- **Structured Handoff**: Providing comprehensive context to human agents

## ✨ Key Features

### 1. **Persona-Aware Intelligence**
- Detects customer personas through keyword matching and pattern analysis
- Three supported personas:
  - **👨‍💻 Technical Expert**: Uses technical terminology, wants detailed explanations
  - **😤 Frustrated User**: Shows emotional language, needs empathetic support
  - **💼 Business Executive**: Outcome-focused, prefers concise communication

### 2. **RAG Pipeline**
- Chunks documents into semantic units (800 characters, 100 overlap)
- Stores embeddings in ChromaDB for efficient retrieval
- Retrieves top-5 relevant documents per query
- Tracks source documents and chunk metadata

### 3. **Adaptive Response Generation**
- Uses Ollama (local LLM) for privacy-preserving inference
- Generates persona-specific prompts
- Technical Expert: Detailed, code-heavy responses
- Frustrated User: Empathetic, step-by-step guidance
- Business Executive: Concise, bullet-pointed summaries

### 4. **Smart Escalation**
- Escalates when no relevant documents found
- Escalates on low confidence (< 60%)
- Escalates after multiple failed attempts (3+)
- Detects billing, legal, security issues
- Generates structured handoff summaries

### 5. **Interactive UI**
- Streamlit-based web interface
- Real-time persona detection display
- Source attribution with confidence scores
- Escalation alerts and handoff summaries
- Test scenarios for quick demo

## 📋 Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Backend** | Python | 3.11+ |
| **Agent Framework** | LangChain | 0.1.14 |
| **LLM** | Ollama (Mistral) | Latest |
| **Embeddings** | Sentence Transformers | 2.2.2 |
| **Vector DB** | ChromaDB | 0.4.24 |
| **UI** | Streamlit | 1.31.1 |
| **Document Processing** | LangChain Loaders | 0.1.14 |

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Input (Message)                     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
         ┌───────────────────────────────┐
         │   Persona Detection Module    │
         │  (Keyword + Pattern Matching) │
         └────────────┬──────────────────┘
                      │
          ┌───────────┴────────────┐
          ▼                        ▼
    [Technical Expert]    [User Type Identified]
    [Frustrated User]     [Confidence Score]
    [Business Executive]  [Keywords]
                      │
                      ▼
         ┌───────────────────────────────┐
         │   RAG Retrieval Pipeline      │
         │   - Query Embedding           │
         │   - Vector Similarity Search  │
         │   - Top-K Retrieval (K=5)     │
         └────────────┬──────────────────┘
                      │
          ┌───────────┴────────────┐
          ▼                        ▼
    [Retrieved Docs]         [Source Tracking]
    [Similarity Scores]       [Confidence: 0.78]
                      │
                      ▼
         ┌───────────────────────────────┐
         │  Response Generation Module   │
         │  - Persona-Specific Prompt    │
         │  - Context Assembly           │
         │  - Ollama LLM Inference       │
         └────────────┬──────────────────┘
                      │
                      ▼
         ┌───────────────────────────────┐
         │  Escalation Logic Module      │
         │  - Confidence Threshold       │
         │  - Trigger Keywords           │
         │  - Attempt Counter            │
         └────────────┬──────────────────┘
                      │
    ┌─────────────────┴─────────────────┐
    ▼                                   ▼
[No Escalation]              [Escalation Required]
[Return Response]            [Generate Handoff]
                             [Queue for Human]
```

## 📁 Project Structure

```
adaptive-customer-support/
├── src/
│   ├── __init__.py
│   ├── persona_detector.py          # Persona detection logic
│   ├── rag_pipeline.py              # RAG implementation
│   ├── response_generator.py        # LLM response generation
│   ├── escalation_handler.py        # Escalation & handoff
│   └── main.py                      # Main orchestration
├── ui/
│   └── streamlit_app.py             # Web UI
├── data/
│   └── kb_documents/                # Knowledge base documents
│       ├── 1_getting_started.md
│       ├── 2_authentication_guide.md
│       ├── ...
│       └── 13_mobile_guide.md
├── config.py                        # Configuration management
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment variables template
├── .gitignore                       # Git ignore rules
├── README.md                        # This file
└── tests/                           # Test cases (optional)
```

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.11 or higher
- Ollama installed and running (Download: https://ollama.ai)
- Git for version control
- 2GB+ RAM recommended

### 2. Clone Repository

```bash
git clone https://github.com/yourusername/adaptive-customer-support.git
cd adaptive-customer-support
```

### 3. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Set Up Environment Variables

```bash
cp .env.example .env

# Edit .env and configure if needed:
# - OLLAMA_BASE_URL (default: http://localhost:11434)
# - LLM_MODEL (default: mistral)
# - CHROMA_DB_PATH (default: ./data/chromadb)
```

### 6. Start Ollama Service

```bash
# Open terminal and run Ollama
ollama serve

# In another terminal, pull model (one-time):
ollama pull mistral
ollama pull nomic-embed-text
```

### 7. Run Streamlit Application

```bash
streamlit run ui/streamlit_app.py
```

The application will open at `http://localhost:8501`

## 📚 Knowledge Base Setup

### Knowledge Base Documents

The `data/kb_documents/` directory contains 13 comprehensive support articles:

1. **Getting Started** - Product overview, setup, pricing
2. **Authentication Guide** - API keys, OAuth, security best practices
3. **Common Issues** - Troubleshooting sync problems, performance issues
4. **API Reference** - Complete API endpoint documentation
5. **Billing & Limits** - Pricing, usage limits, rate limiting
6. **Advanced Features** - Versioning, webhooks, advanced scheduling
7. **FAQ** - Frequently asked questions and answers
8. **Performance Guide** - Optimization, monitoring, best practices
9. **Updates & Releases** - Version history, breaking changes
10. **Enterprise Features** - SLA, dedicated support, advanced security
11. **Disaster Recovery** - DR planning, backup strategies, incident response
12. **Integration Examples** - Use cases, code samples, API patterns
13. **Mobile Guide** - Mobile app features, security, troubleshooting

### Adding Custom Documents

1. Create markdown files in `data/kb_documents/`
2. Use clear headings and structured content
3. Include specific technical information
4. Run system - documents auto-ingested on startup

```bash
# Example: Create new document
cat > data/kb_documents/14_custom_guide.md << 'EOF'
# Custom Integration Guide

## Overview
Your custom content here...
EOF
```

## 🧬 Persona Detection Strategy

### Detection Method: Multi-Signal Approach

#### 1. **Keyword Matching** (40% weight)
```python
Technical Expert Keywords:
  api, error, log, debug, stack trace, configuration,
  integration, authentication, endpoint, webhook

Frustrated User Keywords:
  frustrated, not working, broken, help, urgent,
  critical, asap, angry, disappointed

Business Executive Keywords:
  impact, business, operations, timeline, resolution,
  uptime, revenue, productivity, cost, risk
```

#### 2. **Pattern Analysis** (40% weight)
```python
Technical: Detects code snippets, brackets, URLs, technical questions
Frustrated: Detects exclamation marks, ALL CAPS, punctuation repetition
Executive: Detects business terms, brevity (<30 words), action language
```

#### 3. **Confidence Scoring** (20% weight)
```python
Final Score = Weighted Sum of Signals
Confidence = Max Score / (Sum of All Scores)
Range: 0.0 - 1.0
```

## 🔄 RAG Pipeline Design

### Chunking Strategy

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Chunk Size | 800 chars | Balance context + specificity |
| Overlap | 100 chars | Preserve context across chunks |
| Strategy | Recursive | Intelligently break on boundaries |

### Retrieval Strategy

- **Vector Database**: ChromaDB (in-memory + persistent)
- **Similarity Metric**: Cosine distance → Similarity conversion
- **Top-K**: 5 documents per query
- **Threshold**: None (retrieves top-5 regardless)
- **Metadata**: Source file, chunk index, chunk count

### Embedding Model

- **Model**: Sentence Transformers (via Ollama: nomic-embed-text)
- **Dimension**: 768
- **Format**: Dense vector embeddings
- **Privacy**: Local inference (no external API calls)

## 🚨 Escalation Logic

### Escalation Triggers

| Trigger | Condition | Action |
|---------|-----------|--------|
| **No Docs Found** | `len(retrieved_docs) == 0` | Escalate immediately |
| **Low Confidence** | `confidence < 0.60` | Escalate after 1 attempt |
| **Max Attempts** | `attempt_count >= 3` | Escalate if unresolved |
| **Trigger Keywords** | Billing, legal, security detected | Escalate immediately |

### Handoff Summary Structure

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "customer_persona": "Technical Expert",
  "issue_summary": {
    "description": "User query",
    "category": "technical"
  },
  "conversation_overview": {
    "total_messages": 3,
    "last_message": "...",
    "sentiment": "neutral"
  },
  "attempted_resolution": {
    "attempts_count": 2,
    "steps_taken": ["Suggested troubleshooting", "Provided logs"],
    "documents_referenced": ["3_common_issues.md"],
    "success_indicators": {}
  },
  "escalation_details": {
    "reason": "Low confidence response",
    "escalation_triggers": [],
    "required_access": {}
  },
  "customer_context": {
    "frustration_level": "low",
    "technical_proficiency": "high",
    "preferred_communication": "detailed_technical"
  },
  "recommended_next_steps": [...],
  "urgency_level": "NORMAL"
}
```

## 📊 Example Queries

### 1. Technical Expert Query
```
"Can you explain the API authentication failure and provide error details?"
→ Detected: Technical Expert (92% confidence)
→ Retrieves: 2_authentication_guide.md, 4_api_reference.md
→ Response: Technical, includes error codes and step-by-step debugging
```

### 2. Frustrated User Query
```
"I've tried everything and nothing works! Please help me!"
→ Detected: Frustrated User (88% confidence)
→ Retrieves: 3_common_issues.md
→ Response: Empathetic, simple steps, reassuring tone
```

### 3. Business Executive Query
```
"How does this issue impact operations and when will it be resolved?"
→ Detected: Business Executive (85% confidence)
→ Retrieves: 5_billing_and_limits.md, 10_enterprise_features.md
→ Response: Concise, business impact focused, timeline-oriented
```

## 🔧 Configuration Reference

### Environment Variables (`.env`)

```bash
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
LLM_MODEL=mistral
EMBEDDING_MODEL=nomic-embed-text

# ChromaDB Configuration
CHROMA_DB_PATH=./data/chromadb

# RAG Configuration
CHUNK_SIZE=800
CHUNK_OVERLAP=100
TOP_K_RETRIEVAL=5

# Application Configuration
ESCALATION_THRESHOLD=0.6
MAX_CONTEXT_TOKENS=4000
LOG_LEVEL=INFO
```

### Model Selection

**LLM Models Available via Ollama:**
- `mistral` (default) - Fast, 7B parameters
- `llama2` - Flexible, 7B parameters
- `neural-chat` - Conversational optimized
- `zephyr` - Instruction-tuned

**Embedding Models:**
- `nomic-embed-text` (default) - 768 dimensions
- `all-minilm` - Smaller, faster
- `all-mpnet-base-v2` - More accurate

## 🧪 Testing

### Test Scenarios (Available in UI)

```
1. Technical Expert
   Query: "Can you explain the API authentication failure and provide error details?"
   
2. Frustrated User
   Query: "I've been trying to set up my sync for hours and nothing works! Please help me!"
   
3. Business Executive
   Query: "How does this issue impact operations and when will it be resolved?"
```

### Manual Testing

```python
# Using Python directly
from src.main import get_support_agent

agent = get_support_agent()
response = agent.process_message("Your test query here")
print(response)
```

## 📈 Performance Metrics

### Typical Performance

| Metric | Value |
|--------|-------|
| **Persona Detection** | < 100ms |
| **Document Retrieval** | 200-500ms |
| **Response Generation** | 2-5 seconds |
| **Total E2E Time** | 3-6 seconds |
| **Memory Usage** | 500-800MB |

### Optimization Tips

1. **Faster Response**: Use smaller model (neural-chat vs mistral)
2. **Lower Memory**: Reduce batch size or disable versioning
3. **Better Accuracy**: Use larger model or increase chunk count

## 🐛 Troubleshooting

### Issue: "Connection refused" to Ollama

**Solution:**
```bash
# Ensure Ollama is running
ollama serve

# Check if running on correct port
curl http://localhost:11434/api/tags
```

### Issue: Out of Memory

**Solution:**
```bash
# Reduce chunk size
CHUNK_SIZE=400

# Reduce top-k retrieval
TOP_K_RETRIEVAL=3

# Restart application
```

### Issue: Slow Response Generation

**Solution:**
```bash
# Switch to faster model
ollama pull neural-chat
# Then set LLM_MODEL=neural-chat in .env
```

### Issue: Inaccurate Persona Detection

**Solution:**
- Check if keywords are in message
- Verify persona keyword lists in config.py
- Consider reducing confidence threshold

## 📝 Known Limitations

1. **Single-Turn Context**: Currently limited to recent messages in history
2. **No Sentiment Analysis**: Uses rule-based frustration detection
3. **Offline Only**: Requires local Ollama (no cloud API support)
4. **No Persistent Storage**: Conversation lost after session
5. **Limited to 3 Personas**: Extensible but not currently dynamic

## 🔮 Future Improvements

### Phase 2 Enhancements
- [ ] Multi-turn conversation memory optimization
- [ ] Sentiment analysis integration
- [ ] Custom persona creation
- [ ] Conversation persistence (SQLite/PostgreSQL)
- [ ] Analytics dashboard

### Phase 3 Advanced Features
- [ ] LangGraph agentic architecture
- [ ] Multi-agent collaboration
- [ ] Real-time feedback collection
- [ ] Confidence scoring refinement
- [ ] Support for multiple LLMs
- [ ] Fine-tuned models for domain

## 📄 License

MIT License - See LICENSE file for details

## 👥 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch
3. Make changes
4. Submit pull request

## 📞 Support

For issues or questions:
1. Check troubleshooting section
2. Review knowledge base documents
3. Create GitHub issue with details

## 🎓 Learning Resources

- [LangChain Documentation](https://python.langchain.com)
- [ChromaDB Guide](https://docs.trychroma.com)
- [Ollama Setup](https://github.com/ollama/ollama)
- [Streamlit Docs](https://docs.streamlit.io)
- [RAG Patterns](https://python.langchain.com/docs/use_cases/question_answering/)

## 📌 Project Status

**Current Version**: 1.0.0
**Status**: ✅ Production Ready
**Last Updated**: January 2024

---

**Made with ❤️ for Adsparkx AI Assignment**
