# LangChain + Ollama + ChromaDB (Local Setup)

This repo contains small working examples for:

- Running **local LLMs** using **Ollama + LangChain**
- Streaming responses
- Maintaining chat history
- Basic **ChromaDB** vector DB setup (local)

---

## ✅ Prerequisites

- Python 3.11+
- Ollama installed

---

## 1) Create Virtual Environment

```bash
python3 -m venv py3.11
source py3.11/bin/activate


# Install Dependancies
pip install -U langchain langchain-core langchain-community langchain-ollama
pip install -U chromadb
pip install -U python-dotenv

# Start Ollama
ollama serve

# Pull Models
ollama pull mistral

# Run mitral model on terminal
ollama run mistral

# install chromadb
pip3 install chromadb

# recommendation
python3 -m pip install chromadb

# Setup environments
python3 -m venv env-langchain
source env-langchain/bin/activate

python3 -m pip install chromadb "pydantic<2" langchain
python3 -m pip install langchain-community


python3 -m pip install fastapi uvicorn

# Install a package
pip install langchain

# Install multiple packages
pip install langchain openai requests

# Install specific version
pip install langchain==0.1.0

# Uninstall
pip uninstall langchain

# List installed packages
pip list

# Show package info
pip show langchain

# Save dependencies (like package.json)
pip freeze > requirements.txt

# Install from requirements.txt
pip install -r requirements.txt
