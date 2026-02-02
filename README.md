# 📚 Multi-Agent PDF Assistant with RAG

## 🎯 Project Overview

An intelligent **PDF Assistant** powered by **Retrieval-Augmented Generation (RAG)** that allows users to interact with PDF documents through natural language conversations. Simply upload PDF files or provide URLs, and ask questions about the content - the AI assistant will retrieve relevant information from the documents and provide accurate, context-aware answers.

This application combines the power of:
- **Vector Database (PgVector)** for efficient document storage and semantic search
- **Groq's LLaMA 3.3 70B** for fast, high-quality language model responses
- **GitHub Models** for text embeddings
- **Streamlit** for an intuitive web interface

## PDF Assistant Demo
<img width="1916" height="1027" alt="Screenshot 2026-02-03 012511" src="https://github.com/user-attachments/assets/b74d0c50-a5dd-43c4-bf9e-8829b3c4600e" />


## ✨ Features

- 📤 **Multiple Input Methods**
  - Upload PDF files directly from your computer
  - Provide URLs to online PDF documents

- 💬 **Interactive Chat Interface**
  - Ask questions about your documents in natural language
  - Get accurate answers with context from the PDFs
  - Conversation history maintained during session

- 🧠 **Advanced RAG Pipeline**
  - Automatic document chunking and embedding
  - Semantic search for relevant context
  - PostgreSQL with PgVector for vector storage
  - Efficient retrieval of top-5 most relevant document chunks

- 🎨 **User-Friendly Interface**
  - Clean, modern Streamlit UI
  - Progress indicators for document loading
  - Real-time chat experience
  - Easy document management

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **LLM** | Groq (LLaMA 3.3 70B Versatile) |
| **Embeddings** | GitHub Marketplace Models (text-embedding-3-small) |
| **Vector Database** | PostgreSQL with PgVector |
| **AI Framework** | Phidata |
| **Frontend** | Streamlit |
| **PDF Processing** | PyPDF |
| **Language** | Python 3.12 |

## 📋 Prerequisites

- Python 3.12+
- PostgreSQL with PgVector extension
- Docker (for running PgVector database)
- Groq API key
- GitHub Personal Access Token (for embeddings)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd "Multi Agentic AI RAG With Vector Databse"
```

### 2. Create Virtual Environment
```bash
# Using UV (recommended)
uv venv --python 3.12
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Or using standard Python
python -m venv .venv
.venv\Scripts\activate  # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up PgVector Database
Run the PostgreSQL database with PgVector extension using Docker:

```bash
docker run -d \
  -e POSTGRES_DB=ai \
  -e POSTGRES_USER=ai \
  -e POSTGRES_PASSWORD=ai \
  -e PGDATA=/var/lib/postgresql/data/pgdata \
  -v pgvolume:/var/lib/postgresql/data \
  -p 5532:5432 \
  --name pgvector \
  phidata/pgvector:16
```

### 5. Configure Environment Variables
Create a `.env` file in the project root:

```env
GROQ_API_KEY="your_groq_api_key_here"
GITHUB_TOKEN="your_github_personal_access_token_here"
```

**Getting API Keys:**
- **Groq API Key**: Sign up at [Groq Console](https://console.groq.com)
- **GitHub Token**: Generate at [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)

## 💻 Usage

### Run the Streamlit App
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Using the Application

1. **Load Documents**
   - Choose either "Upload PDFs" or "Provide URLs" in the sidebar
   - For uploads: Select PDF files from your computer
   - For URLs: Paste PDF URLs (one per line)
   - Click "Load PDFs" or "Load URLs" button
   - Wait for the success message

2. **Ask Questions**
   - Type your question in the chat input at the bottom
   - The assistant will search the documents and provide answers
   - Continue the conversation naturally

3. **Clear Conversation**
   - Click "🗑️ Clear Conversation" button in the sidebar to reset

### Example Questions
- "What is this document about?"
- "Summarize the main points"
- "Find information about [specific topic]"
- "What are the key findings?"
- "Explain [concept] from the document"

## 📁 Project Structure

```
Multi Agentic AI RAG With Vector Databse/
├── app.py                  # Streamlit web application
├── pdf_assistant.py        # CLI version of the assistant
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## 🔧 Configuration

### Database Connection
Default connection string in `app.py`:
```python
db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"
```

Modify if you're using different credentials or port.

### Model Selection
To change the LLM model, edit the `Groq` initialization:
```python
llm=Groq(model="llama-3.3-70b-versatile")
```

**Other available Groq models:**
- `llama-3.1-70b-versatile`
- `mixtral-8x7b-32768`
- `gemma2-9b-it`

### Retrieval Settings
Adjust the number of relevant documents retrieved:
```python
relevant_docs = kb.search(query=prompt, num_documents=5)  # Change 5 to your preference
```

## 🐛 Troubleshooting

### Issue: "Added 0 documents to knowledge base"
**Solution**: Ensure PDFs contain extractable text (not just images). The app uses text extraction, not OCR.

### Issue: API Key Errors
**Solution**: 
- Verify `.env` file exists and contains correct API keys
- Ensure no extra spaces in key values
- Restart the Streamlit app after updating `.env`

### Issue: Database Connection Failed
**Solution**:
- Check if Docker container is running: `docker ps`
- Verify port 5532 is not in use
- Ensure PgVector container started successfully

### Issue: Import Errors
**Solution**: Reinstall dependencies
```bash
pip install -r requirements.txt --upgrade
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- [Phidata](https://github.com/phidatahq/phidata) - AI application framework
- [Groq](https://groq.com/) - Fast LLM inference
- [Streamlit](https://streamlit.io/) - Web framework
- [PgVector](https://github.com/pgvector/pgvector) - Vector similarity search

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Built with ❤️ using Phidata, Groq, and Streamlit**
