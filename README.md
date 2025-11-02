📘 PDF RAG Assistant (ChromaDB + Groq)

An intelligent Retrieval-Augmented Generation (RAG) application that lets you upload any PDF and ask natural language questions about its content — powered by Groq’s LLaMA models and ChromaDB.

🚀 Overview

The PDF RAG Assistant extracts text from uploaded PDFs, converts it into semantic embeddings using SentenceTransformers, stores those embeddings in ChromaDB, retrieves the most relevant chunks for a given query, and uses Groq’s LLaMA models to generate context-based answers.

It’s a lightweight, secure, and explainable mini-RAG pipeline ideal for:

🎓 Students learning RAG fundamentals

💼 Developers building AI document assistants

🧠 Interview portfolios demonstrating applied AI projects

🧩 Key Features

✅ PDF Text Extraction – Reads and processes text from any uploaded PDF file
✅ Text Chunking – Splits content into smaller, meaningful segments for efficient search
✅ Vector Embedding – Converts text chunks into numerical embeddings using SentenceTransformers
✅ Semantic Search (ChromaDB) – Retrieves contextually relevant chunks for any question
✅ LLM Response Generation (Groq) – Generates accurate, context-based answers using Groq-hosted LLaMA models
✅ Interactive Streamlit UI – Clean chat-style interface with chat history
✅ Privacy First – PDF data stays local; only the question + selected chunks are sent to Groq API

💡 Use Cases

📄 Document Q&A: Quickly understand long PDFs (research papers, policies, manuals)

🧾 Contract & Policy Review: Extract specific insights from large documents

🧠 Study Companion: Ask questions from lecture notes or textbooks

🧰 Enterprise RAG Demo: Foundation for building internal knowledge retrieval systems

🧱 System Architecture
🔭 High-Level Flow
User → Streamlit UI → PDF Extractor → Chunker → Embeddings → ChromaDB
       ↑                                     ↓
     Chat UI ← Groq API (LLaMA) ← Context + Question

🏗️ Architecture Diagram
               ┌────────────────────────────────────────┐
               │             Streamlit UI                │
               │  - Upload PDF                           │
               │  - Enter Groq API Key                   │
               │  - Ask Question                         │
               └───────────────┬─────────────────────────┘
                               │
                               ▼
              ┌────────────────────────────────────────┐
              │          PDF Text Extractor             │
              │  • Extracts text using PyPDF2           │
              └───────────────┬─────────────────────────┘
                               │
                               ▼
              ┌────────────────────────────────────────┐
              │          Text Chunking Engine           │
              │  • Splits text into 500-word chunks     │
              └───────────────┬─────────────────────────┘
                               │
                               ▼
              ┌────────────────────────────────────────┐
              │      Embedding Generation (AI Model)    │
              │  • Uses SentenceTransformer model        │
              └───────────────┬─────────────────────────┘
                               │
                               ▼
              ┌────────────────────────────────────────┐
              │         ChromaDB Vector Store           │
              │  • Stores embeddings persistently       │
              └───────────────┬─────────────────────────┘
                               │
                               ▼
              ┌────────────────────────────────────────┐
              │          Query Retrieval Engine         │
              │  • Embeds user query                    │
              │  • Retrieves top-k relevant chunks      │
              └───────────────┬─────────────────────────┘
                               │
                               ▼
              ┌────────────────────────────────────────┐
              │           Groq API (LLM Engine)         │
              │  • Generates precise answers             │
              └───────────────┬─────────────────────────┘
                               │
                               ▼
              ┌────────────────────────────────────────┐
              │          Streamlit Chat Output          │
              │  • Displays answer + chat history       │
              └────────────────────────────────────────┘

🧠 Features in Detail
Module	Description
Streamlit UI	Interactive dashboard for uploading PDFs and chatting with the assistant.
PyPDF2 Extractor	Extracts plain text from all PDF pages.
Chunking Engine	Breaks long text into smaller parts for embedding.
SentenceTransformer	Converts text into semantic embeddings.
ChromaDB	Vector database used to store and retrieve embeddings efficiently.
Groq API	Uses Groq’s LLaMA models for contextual understanding and generation.
Chat Memory	Maintains Q&A history for each session.
🛡️ Security & Privacy

🔒 Local Data Storage – All PDF content and embeddings stay local in ./chroma_store.
🔑 Secure API Handling – Groq API key is session-based and never saved.
🧹 Temporary File Handling – Uploaded PDFs are stored temporarily and deleted automatically.
🚫 No Cloud Uploads – No external cloud data storage used (only Groq API request).

⚙️ Technology Stack
Layer	Technology
Frontend/UI	Streamlit
Text Extraction	PyPDF2
Vectorization	SentenceTransformers (all-MiniLM-L6-v2)
Vector Database	ChromaDB
LLM API	Groq API (LLaMA series models)
Language	Python 3.10+
📦 Installation & Setup
1️⃣ Clone Repository
git clone https://github.com/sandhyagunti/pdf-rag-assistant.git
cd pdf-rag-assistant

2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate      # For macOS/Linux
venv\Scripts\activate         # For Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run the App
streamlit run app.py

5️⃣ Open in Browser

The app will open automatically at:
👉 http://localhost:8501

🧾 Requirements.txt
streamlit==1.38.0
requests==2.32.3
PyPDF2==3.0.1
chromadb==0.5.3
sentence-transformers==3.0.1
torch==2.4.1
numpy==1.26.4

🧠 Example Prompt Flow

Upload PDF → app extracts and embeds text

Ask: “Summarize chapter 2.”

App retrieves top matching chunks

Sends combined context + query to Groq API

Displays contextual answer

🧩 Architecture Summary
Step	Module	Description
1	Upload PDF	User uploads document via Streamlit UI
2	Extract Text	PyPDF2 reads and extracts text
3	Chunk & Embed	Text split & encoded via SentenceTransformer
4	Store in ChromaDB	Vectors stored locally for retrieval
5	Query Retrieval	Finds semantically similar chunks
6	Groq API Call	Generates natural language answer
7	Display Output	Shows final answer and saves chat history
🌐 Future Enhancements

🧩 Multi-PDF Support

🔍 Improved retrieval ranking

🧠 Fine-tuned local models (for offline mode)

💬 Persistent chat memory

🧾 Source citation display

👨‍💻 Author

Sandhya Gunti
📧 AI Developer | Data Science Enthusiast
💡 Focused on building intelligent, privacy-first AI assistants.
