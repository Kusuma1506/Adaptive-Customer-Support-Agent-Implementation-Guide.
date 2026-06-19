#!/usr/bin/env python3
"""
Quick Start Script for Persona-Adaptive Support Agent

This script sets up the environment and starts the application.
Run: python run.py
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(text)
    print("="*60)

def check_python_version():
    """Check Python version"""
    print_header("📋 Checking Python Version")
    
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print("❌ Python 3.11 or higher required")
        return False
    
    print("✅ Python version OK")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    print_header("📦 Checking Dependencies")
    
    required = ['streamlit', 'chromadb', 'langchain', 'requests']
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - missing")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies OK")
    return True

def check_ollama():
    """Check if Ollama is running"""
    print_header("🔌 Checking Ollama Connection")
    
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"✅ Connected to Ollama")
            print(f"Available models: {len(models)}")
            
            # Check for required models
            model_names = [m.get('name', '').split(':')[0] for m in models]
            
            if 'mistral' in model_names:
                print("✅ Mistral model available")
            else:
                print("⚠️  Mistral model not found")
                print("Run: ollama pull mistral")
            
            if 'nomic-embed-text' in model_names:
                print("✅ Embedding model available")
            else:
                print("⚠️  Embedding model not found")
                print("Run: ollama pull nomic-embed-text")
            
            return True
        else:
            print("❌ Cannot connect to Ollama")
            return False
            
    except Exception as e:
        print(f"❌ Ollama not running: {str(e)}")
        print("\nTo start Ollama:")
        if platform.system() == "Windows":
            print("1. Download: https://ollama.ai")
            print("2. Run: ollama serve")
        else:
            print("Run: ollama serve")
        return False

def check_knowledge_base():
    """Check if knowledge base exists"""
    print_header("📚 Checking Knowledge Base")
    
    kb_path = Path("data/kb_documents")
    
    if kb_path.exists():
        files = list(kb_path.glob("*.md"))
        print(f"✅ Knowledge base directory exists")
        print(f"Documents found: {len(files)}")
        
        for f in files[:3]:
            print(f"  - {f.name}")
        
        if len(files) > 3:
            print(f"  ... and {len(files) - 3} more")
        
        return len(files) > 0
    else:
        print("❌ Knowledge base directory not found")
        return False

def check_environment_file():
    """Check if .env file exists"""
    print_header("🔐 Checking Environment Configuration")
    
    env_path = Path(".env")
    example_path = Path(".env.example")
    
    if env_path.exists():
        print("✅ .env file exists")
        return True
    elif example_path.exists():
        print("⚠️  .env file missing (using defaults)")
        print("Copy .env.example to .env to customize")
        return True
    else:
        print("❌ Environment files missing")
        return False

def run_verification():
    """Run all checks"""
    print_header("🔍 Pre-Launch Verification")
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Knowledge Base", check_knowledge_base),
        ("Environment", check_environment_file),
        ("Ollama Service", check_ollama),
    ]
    
    results = []
    
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"❌ Error in {check_name}: {str(e)}")
            results.append((check_name, False))
    
    print_header("✅ Verification Summary")
    
    all_passed = True
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {check_name}")
        if not result:
            all_passed = False
    
    return all_passed

def start_application():
    """Start the Streamlit application"""
    print_header("🚀 Starting Application")
    
    print("Launching Streamlit UI on http://localhost:8501")
    print("Press Ctrl+C to stop\n")
    
    cmd = ["streamlit", "run", "ui/streamlit_app.py"]
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n\n👋 Application stopped")

def main():
    """Main entry point"""
    print("\n")
    print(" " * 12 + "🤖 Persona-Adaptive Support Agent")
    print(" " * 15 + "Quick Start Script")
    print(" " * 20 + "v1.0.0")
    
    # Run verification
    if not run_verification():
        print("\n❌ Verification failed. Please fix the issues above.")
        print("\nFor help, see README.md")
        sys.exit(1)
    
    # Start application
    print("\n" + "="*60)
    start_or_cli = input("\nStart (S)treamilit UI or (C)LI interface? (s/c): ").strip().lower()
    
    if start_or_cli == 'c':
        print("Launching CLI interface...\n")
        from src.cli import CLIInterface
        cli = CLIInterface()
        cli.run()
    else:
        start_application()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
