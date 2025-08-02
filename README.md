
# 🔍 LLM Query–Retrieval System using Gemini

A powerful LLM-based system that allows users to upload documents (PDF, DOCX, Emails via URL), ask natural language questions, and get semantically accurate answers with source context.

Built with:

- 📦 FastAPI backend
- 🧠 Gemini 2.0 Flash for reasoning
- 🧬 Instructor-XL for embeddings
- ⚡ FAISS for vector similarity search
- 🖥️ Streamlit frontend for simple UI
- 📄 Supports PDF, DOCX, and email text

---

## 🏗️ Project Structure

```

llm-query-retrieval-gemini/
│
├── app/
│   ├── main.py                  # FastAPI app entry point
│   ├── config.py                # Loads env vars
│   ├── models.py                # Pydantic models
│   ├── routes/
│   │   └── query.py             # /hackrx/run endpoint
│   ├── services/
│   │   ├── parser.py            # PDF, DOCX, email text extractor
│   │   ├── chunker.py           # Semantic chunking
│   │   ├── embedder.py          # Embeds using Instructor-XL
│   │   ├── vector\_store.py      # FAISS-based retrieval
│   │   ├── llm\_decider.py       # Gemini answer engine
│   │   └── json\_formatter.py    # Formats output
│   └── utils/
│       ├── downloader.py        # Blob/text downloader
│       └── logger.py            # Logger
│
├── ui/
│   └── streamlit\_app.py         # Frontend app
│
├── tests/                       # Unit tests
├── sample\_input.json            # Sample request for testing
├── requirements.txt             # Python dependencies
├── .env                         # Env vars (API key, etc.)
└── README.md                    # This file

````

---

## ⚙️ Setup Instructions

### ✅ Prerequisites

- Python 3.10+
- `pip` or `venv` installed
- Virtual environment (recommended)

---

### 🚀 Step 1: Clone and Setup

```bash
git clone https://github.com/your-username/llm-query-retrieval-gemini.git
cd llm-query-retrieval-gemini
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
````

---

### 📦 Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 🔐 Step 3: Create `.env` file

Create a `.env` file in the root directory with:

```env
# API Key from Google AI Console
GEMINI_API_KEY=your_gemini_api_key

# Optional: Set endpoint for frontend to call
API_ENDPOINT=http://localhost:8000/hackrx/run
```

---

### 🧠 Step 4: Run FastAPI Backend

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8001
```

ngrok http 8001

It will start at: [http://localhost:8000](http://localhost:8000)

---

### 💻 Step 5: Run Streamlit Frontend

```bash
streamlit run ui/streamlit_app.py
```

Go to: [http://localhost:8501](http://localhost:8501)

---

## 🧪 Running Tests

```bash
pytest tests/
```

---

## 📤 Sample Input (JSON)

```json
{
  "documents": "https://example.com/document.pdf",
  "questions": [
    "What is the refund policy?",
    "When does the agreement expire?"
  ]
}
```

---

## 📌 Notes

* You can plug in **Google Gemini Pro/Flash** via the API key.
* Supports hierarchical outlines and chunked retrieval.
* Extend to file uploads, vector DB persistence, or multi-modal models.

---

## 📄 License

MIT © 2025 
---

## ✅ Summary: How to Run

| Task         | Command                             |
| ------------ | ----------------------------------- |
| 🔧 Setup     | `pip install -r requirements.txt`   |
| 🧠 Backend   | `uvicorn app.main:app --reload`     |
| 🖥️ Frontend | `streamlit run ui/streamlit_app.py` |
| 🧪 Tests     | `pytest tests/`                     |

---
## Sample Images

### UI
<img width="491" height="578" alt="image" src="https://github.com/user-attachments/assets/323a382d-9018-4856-a175-85b792381ff4" />

