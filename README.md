# RAGnosis 🔍📄  
**LLM-powered Retrieval-Augmented Generation (RAG) System for Intelligent Document & Web Querying**

---

## 📌 Project Overview
**RAGnosis** is an intelligent question-answering system built using **Large Language Models (LLMs)** and **Retrieval-Augmented Generation (RAG)** techniques.  
The system allows users to upload **PDF documents** and provide **URLs**, automatically extracts and indexes the content, and enables accurate, context-aware responses based strictly on the provided knowledge base.

Unlike generic chatbots, RAGnosis minimizes hallucinations by grounding responses in user-supplied data, making it suitable for research, academic, and enterprise use cases.

---

## 🎯 Problem Statement
Traditional LLMs:
- Lack access to private or domain-specific documents
- Produce hallucinated or unverifiable answers
- Cannot efficiently scale to large document collections

**RAGnosis** addresses these limitations by:
- Combining semantic search with LLM reasoning
- Persistently storing document embeddings
- Answering queries only from trusted sources

---

## 🧠 Solution Approach (RAG Architecture)
1. **Data Ingestion**
   - PDFs are parsed and text is extracted
   - URLs are crawled and cleaned
2. **Chunking & Embeddings**
   - Documents are split into semantic chunks
   - Embeddings are generated using transformer-based models
3. **Vector Storage**
   - Embeddings are stored in a vector database (FAISS)
4. **Query Pipeline**
   - User query is embedded
   - Relevant chunks are retrieved via similarity search
   - Retrieved context is passed to the LLM for grounded answers

## 🛠️ Tech Stack
### Backend
- **Python**
- **FastAPI** – API backend
- **LangChain** – RAG orchestration
- **FAISS** – Vector similarity search
- **PyPDF** – PDF parsing

### LLM & NLP
- **LLM via Ollama (Mistral / Phi-3)**
- **Transformer-based Embeddings**

### Frontend
- **HTML, CSS, JavaScript**
- Lightweight chat-style UI

---

## 🚀 Features
- 📄 Upload and query PDF documents
- 🌐 Query content from web URLs
- 🧠 Context-aware, grounded LLM responses
- 💾 Persistent vector storage (no re-processing every run)
- ⚡ Fast and scalable semantic search
- 🔒 Local LLM support for data privacy

---

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Shreyash584/RAGnosis.git
cd RAGnosis
