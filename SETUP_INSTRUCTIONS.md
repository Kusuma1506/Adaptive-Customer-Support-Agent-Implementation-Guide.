# SETUP_INSTRUCTIONS.md

# 🚀 Complete Setup Instructions

## Prerequisites

Before starting, ensure you have:
- Windows/macOS/Linux operating system
- Python 3.11 or higher
- Internet connection (for first-time setup)
- At least 2GB RAM available
- 500MB free disk space

## Step 1: Install Ollama

### Windows
1. Download Ollama from https://ollama.ai
2. Run the installer
3. Accept the default installation path
4. Restart your computer (if prompted)

### macOS
1. Download Ollama from https://ollama.ai
2. Open the .dmg file
3. Drag Ollama to Applications
4. Launch Ollama from Applications

### Linux
```bash
curl https://ollama.ai/install.sh | sh
```

## Step 2: Pull Required Models

After Ollama is installed, open terminal/PowerShell and run:

```bash
# Pull the LLM model
ollama pull mistral

# Pull the embedding model
ollama pull nomic-embed-text
```

These commands will download the models (may take 5-10 minutes depending on internet speed).

## Step 3: Clone Repository

```bash
git clone https://github.com/yourusername/adaptive-customer-support.git
cd adaptive-customer-support
```

## Step 4: Create Virtual Environment

### Windows (PowerShell)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

## Step 5: Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install:
- LangChain and dependencies
- ChromaDB for vector storage
- Streamlit for web UI
- Ollama client
- And all other required packages

## Step 6: Configure Environment (Optional)

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your preferences (optional)
# Default settings should work for most users
```

## Step 7: Start Ollama Service

In a terminal window, run:

```bash
ollama serve
```

Leave this window open - Ollama needs to be running while using the support agent.

## Step 8: Run the Application

Open a NEW terminal window (keeping Ollama running in the first one):

### Option A: Streamlit Web UI (Recommended)
```bash
# Activate virtual environment if not already active
# Then run:
streamlit run ui/streamlit_app.py
```

The application will open in your default browser at `http://localhost:8501`

### Option B: CLI Interface
```bash
python -m src.cli
```

### Option C: Quick Start Script
```bash
python run.py
```

This will verify your setup and let you choose between CLI or Streamlit.

## Verification Checklist

- [ ] Python 3.11+ installed: `python --version`
- [ ] Virtual environment created and activated
- [ ] Dependencies installed: `pip list | grep -E "streamlit|langchain|chromadb"`
- [ ] Ollama running: `curl http://localhost:11434/api/tags`
- [ ] Models available: Check Ollama terminal output
- [ ] Application started: See URL in terminal

## Troubleshooting

### Issue: "Ollama not running"
**Solution:**
```bash
# Verify Ollama is accessible
curl http://localhost:11434/api/tags

# If that fails, start Ollama in another terminal:
ollama serve
```

### Issue: "ModuleNotFoundError"
**Solution:**
```bash
# Ensure virtual environment is activated
python -m pip install -r requirements.txt
```

### Issue: "Port 8501 already in use"
**Solution:**
```bash
# Run on different port
streamlit run ui/streamlit_app.py --server.port 8502
```

### Issue: "Out of memory"
**Solution:**
Edit `.env` and reduce:
```
CHUNK_SIZE=400
TOP_K_RETRIEVAL=3
```

### Issue: "Model not found"
**Solution:**
```bash
ollama pull mistral
ollama pull nomic-embed-text
```

## Test the Installation

### Quick Test
```bash
python -c "from src.main import initialize_support_system; print(initialize_support_system())"
```

Expected output:
```
{'status': 'initialized', 'knowledge_base': {'total_chunks': XXX, ...}, 'agent_ready': True}
```

### Run Demo Scenario
1. Open Streamlit UI
2. Click "Load test message" in sidebar
3. Select "Technical Expert" scenario
4. Click "Use Test Message"
5. System should process and display response

## Next Steps

1. **Read the README.md** for detailed documentation
2. **Try test scenarios** in the UI sidebar
3. **Create custom queries** to test different personas
4. **Review knowledge base** documents in `data/kb_documents/`

## Common Commands

```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
.\venv\Scripts\Activate.ps1  # Windows PowerShell

# Run Streamlit UI
streamlit run ui/streamlit_app.py

# Run CLI
python -m src.cli

# Start Ollama
ollama serve

# Pull a model
ollama pull modelname

# List available models
ollama list
```

## Performance Notes

- **First startup**: May take 10-20 seconds (models loading)
- **Response time**: 3-6 seconds per query (depends on Ollama performance)
- **Memory usage**: 500-800MB typical
- **CPU usage**: 30-50% during response generation

## For Windows Users

If you see PowerShell execution policy errors:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Getting Help

1. Check README.md troubleshooting section
2. Review logs in terminal output
3. Check Ollama terminal for errors
4. Verify all prerequisites are installed

## Production Deployment

For production use:
1. Switch from SQLite to PostgreSQL (optional)
2. Deploy with Gunicorn/Uvicorn
3. Use environment variables for secrets
4. Set up proper logging
5. Consider using GPU acceleration

---

**Questions? Check README.md or review setup troubleshooting section above.**
