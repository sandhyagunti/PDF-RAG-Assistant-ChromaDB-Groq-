import streamlit as st
import tempfile
import requests
from PyPDF2 import PdfReader
import chromadb
from sentence_transformers import SentenceTransformer

# ----------------------- 🔧 Streamlit Config -----------------------
st.set_page_config(page_title="📘PDF RAG Assistant", page_icon="📚", layout="wide")

# Initialize session state
if "collection" not in st.session_state:
    st.session_state["collection"] = None
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# ----------------------- ⚙️ Groq Model Settings -----------------------
model_configs = {
                "llama-3.1-8b-instant": {"max_tokens": 2000, "temperature": 0.1},
                "llama-3.2-1b-preview": {"max_tokens": 2000, "temperature": 0.1},
                "llama-3.2-3b-preview": {"max_tokens": 2000, "temperature": 0.1},
                "llama-3.3-70b-versatile": {"max_tokens": 1500, "temperature": 0.1},
                "llama-guard-3-8b": {"max_tokens": 2000, "temperature": 0.1},
                "mixtral-8x7b-32768": {"max_tokens": 2000, "temperature": 0.1}
            }

# ----------------------- 📄 PDF Functions -----------------------
def extract_pdf_text(file_path):
    """Extract text from PDF pages."""
    reader = PdfReader(file_path)
    return " ".join([page.extract_text() or "" for page in reader.pages]).strip()

def chunk_text(text, size=500):
    """Split large text into smaller overlapping chunks."""
    words = text.split()
    return [" ".join(words[i:i + size]) for i in range(0, len(words), size)]

# ----------------------- 🧠 ChromaDB Embeddings -----------------------
def create_chromadb_collection(text):
    """Store text chunks and embeddings in ChromaDB."""
    client = chromadb.PersistentClient(path="./chroma_store")
    collection = client.get_or_create_collection("pdf_chunks")
    embedder = SentenceTransformer("all-MiniLM-L6-v2")

    chunks = chunk_text(text)
    embeddings = embedder.encode(chunks).tolist()

    collection.upsert(
        ids=[f"chunk_{i}" for i in range(len(chunks))],
        documents=chunks,
        embeddings=embeddings,
    )
    return collection

def retrieve_chunks(collection, query, top_k=2):
    """Retrieve most relevant text chunks from ChromaDB."""
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    query_emb = embedder.encode([query]).tolist()
    results = collection.query(query_embeddings=query_emb, n_results=top_k)
    return results["documents"][0] if results["documents"] else []

# ----------------------- 🤖 Groq API Query -----------------------
def query_groq(api_key, model, prompt):
    """Send query to Groq API and return the response."""
    config = model_configs[model]
    MAX_INPUT_CHARS = 14000  # to prevent token limit errors
    if len(prompt) > MAX_INPUT_CHARS:
        prompt = prompt[:MAX_INPUT_CHARS]
        st.warning("⚠️ Input truncated to fit Groq API limits.")

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": config["max_tokens"],
            "temperature": config["temperature"],
        },
    )

    if response.ok:
        return response.json()["choices"][0]["message"]["content"]
    else:
        st.error(f"Groq API error: {response.status_code} - {response.text}")
        return None

# ----------------------- 🎨 Sidebar UI -----------------------
st.sidebar.header("⚙️ Configuration")

api_key = st.sidebar.text_input("🔑 Groq API Key", type="password")
model = st.sidebar.selectbox("🧠 Choose Model", list(model_configs.keys()))
uploaded_pdf = st.sidebar.file_uploader("📄 Upload PDF", type=["pdf"])

if uploaded_pdf:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
        temp.write(uploaded_pdf.read())
        pdf_path = temp.name

    st.sidebar.info("🔍 Extracting text from PDF...")
    pdf_text = extract_pdf_text(pdf_path)

    st.sidebar.info("💾 Creating ChromaDB collection...")
    st.session_state["collection"] = create_chromadb_collection(pdf_text)
    st.sidebar.success("✅ PDF uploaded and processed successfully!")

# ----------------------- 💬 Main Chat UI -----------------------
st.title("📚  PDF RAG Assistant (ChromaDB + Groq)")
st.caption("Upload a PDF, and ask context-based questions powered by Groq + ChromaDB.")

question = st.text_input("💭 Ask a question about your PDF")

if st.button("🔍 Get Answer"):
    if not api_key:
        st.error("Please enter your Groq API Key.")
    elif not uploaded_pdf:
        st.error("Please upload a PDF file first.")
    elif not question.strip():
        st.error("Please type a question.")
    elif not st.session_state["collection"]:
        st.error("PDF not processed yet.")
    else:
        context = "\n\n".join(retrieve_chunks(st.session_state["collection"], question))
        full_prompt = f"Answer the question using only this context:\n\n{context}\n\nQuestion: {question}"
        answer = query_groq(api_key, model, full_prompt)

        if answer:
            st.session_state["chat_history"].append({"q": question, "a": answer})
            st.success("✅ Answer generated successfully!")
            st.write(answer)

# ----------------------- 📜 Chat History -----------------------
if st.session_state["chat_history"]:
    st.subheader("🧾 Chat History")
    for i, chat in enumerate(st.session_state["chat_history"], 1):
        st.markdown(f"**Q{i}:** {chat['q']}")
        st.markdown(f"**A{i}:** {chat['a']}")
        st.divider()
