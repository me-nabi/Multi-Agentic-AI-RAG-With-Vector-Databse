import streamlit as st
import os
from dotenv import load_dotenv
from phi.assistant import Assistant
from phi.storage.assistant.postgres import PgAssistantStorage
from phi.knowledge.pdf import PDFUrlKnowledgeBase, PDFKnowledgeBase
from phi.vectordb.pgvector import PgVector2
from phi.llm.groq import Groq
from phi.embedder.openai import OpenAIEmbedder
from phi.document.reader.pdf import PDFReader
import tempfile
from typing import List

# Load environment variables
load_dotenv()

# Configure API keys and database
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

# Configure GitHub Marketplace Models for embeddings
token = os.getenv("GITHUB_TOKEN")
endpoint = "https://models.github.ai/inference"

# Page configuration
st.set_page_config(
    page_title="PDF Assistant",
    page_icon="📚",
    layout="wide"
)

st.title("📚 PDF Assistant with RAG")
st.markdown("Upload PDFs or provide URLs to chat with your documents")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "assistant" not in st.session_state:
    st.session_state.assistant = None
if "knowledge_base_loaded" not in st.session_state:
    st.session_state.knowledge_base_loaded = False
if "collection_name" not in st.session_state:
    import uuid
    st.session_state.collection_name = f"docs_{str(uuid.uuid4())[:8]}"

# Sidebar for PDF input
with st.sidebar:
    st.header("📄 Add Documents")
    
    input_method = st.radio("Choose input method:", ["Upload PDFs", "Provide URLs"])
    
    if input_method == "Upload PDFs":
        uploaded_files = st.file_uploader(
            "Upload PDF files",
            type=['pdf'],
            accept_multiple_files=True
        )
        
        if uploaded_files and st.button("Load PDFs"):
            with st.spinner("Loading PDFs and creating knowledge base..."):
                try:
                    st.info(f"📥 Uploading {len(uploaded_files)} file(s)...")
                    # Save uploaded files temporarily
                    temp_paths = []
                    for uploaded_file in uploaded_files:
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                            tmp_file.write(uploaded_file.getvalue())
                            temp_paths.append(tmp_file.name)
                    
                    st.info("🔧 Creating knowledge base...")
                    # Create knowledge base with uploaded files
                    knowledge_base = PDFKnowledgeBase(
                        path=temp_paths,
                        reader=PDFReader(chunk=True),
                        vector_db=PgVector2(
                            collection=st.session_state.collection_name,
                            db_url=db_url,
                            embedder=OpenAIEmbedder(
                                model="text-embedding-3-small",
                                api_key=token,
                                base_url=endpoint
                            )
                        )
                    )
                    
                    st.info("📚 Loading documents into vector database (this may take a moment)...")
                    knowledge_base.load()
                    
                    # Create storage
                    storage = PgAssistantStorage(
                        table_name="pdf_assistant_streamlit",
                        db_url=db_url
                    )
                    
                    # Create assistant
                    st.session_state.assistant = Assistant(
                        llm=Groq(model="llama-3.3-70b-versatile"),
                        knowledge_base=knowledge_base,
                        storage=storage,
                        show_tool_calls=False,
                        search_knowledge=False,
                        read_chat_history=True,
                    )
                    
                    st.session_state.knowledge_base_loaded = True
                    st.session_state.messages = []
                    st.success(f"✅ Loaded {len(uploaded_files)} PDF(s) successfully!")
                    
                    # Clean up temp files
                    for path in temp_paths:
                        try:
                            os.unlink(path)
                        except:
                            pass
                            
                except Exception as e:
                    st.error(f"❌ Error loading PDFs: {str(e)}")
                    import traceback
                    st.error(f"Details: {traceback.format_exc()}")
    
    else:  # Provide URLs
        st.markdown("Enter PDF URLs (one per line):")
        url_input = st.text_area(
            "PDF URLs",
            placeholder="https://example.com/document.pdf\nhttps://example.com/another.pdf",
            height=150
        )
        
        if st.button("Load URLs"):
            if url_input.strip():
                with st.spinner("Loading PDFs from URLs and creating knowledge base..."):
                    try:
                        # Parse URLs
                        urls = [url.strip() for url in url_input.split('\n') if url.strip()]
                        st.info(f"🔗 Processing {len(urls)} URL(s)...")
                        
                        st.info("🔧 Creating knowledge base...")
                        # Create knowledge base with URLs
                        knowledge_base = PDFUrlKnowledgeBase(
                            urls=urls,

                            vector_db=PgVector2(
                                collection=st.session_state.collection_name,
                                db_url=db_url,
                                embedder=OpenAIEmbedder(
                                    model="text-embedding-3-small",
                                    api_key=token,
                                    base_url=endpoint
                                )
                            )
                        )
                        
                        st.info("📚 Downloading and loading documents into vector database (this may take a moment)...")
                        knowledge_base.load()
                        
                        # Create storage
                        storage = PgAssistantStorage(
                            table_name="pdf_assistant_streamlit",
                            db_url=db_url
                        )
                        
                        # Create assistant
                        st.session_state.assistant = Assistant(
                            llm=Groq(model="llama-3.3-70b-versatile"),
                            knowledge_base=knowledge_base,
                            storage=storage,
                            show_tool_calls=False,
                            search_knowledge=False,
                            read_chat_history=True,
                        )
                        
                        st.session_state.knowledge_base_loaded = True
                        st.session_state.messages = []
                        st.success(f"✅ Loaded {len(urls)} URL(s) successfully!")
                        
                    except Exception as e:
                        st.error(f"❌ Error loading URLs: {str(e)}")
                        import traceback
                        st.error(f"Details: {traceback.format_exc()}")
            else:
                st.warning("Please enter at least one URL")
    
    st.divider()
    
    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()
    
    if st.session_state.knowledge_base_loaded:
        st.success("✅ Knowledge base loaded!")
    else:
        st.info("👆 Load documents to start chatting")

# Main chat interface
if st.session_state.knowledge_base_loaded:
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask a question about your documents..."):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Manually search the knowledge base
                    kb = st.session_state.assistant.knowledge_base
                    relevant_docs = kb.search(query=prompt, num_documents=5)
                    
                    # Build context from relevant documents
                    context = "\n\n".join([f"Document {i+1}:\n{doc.content}" for i, doc in enumerate(relevant_docs)])
                    
                    # Create enhanced prompt with context
                    enhanced_prompt = f"""Based on the following context from the documents, please answer the question.

Context:
{context}

Question: {prompt}

Answer:"""
                    
                    # Run the assistant and get response
                    response = st.session_state.assistant.run(enhanced_prompt, stream=False)
                    
                    # Extract the response content properly
                    if hasattr(response, 'content'):
                        response_text = response.content
                    elif hasattr(response, 'messages') and len(response.messages) > 0:
                        # Get the last message content
                        last_message = response.messages[-1]
                        if hasattr(last_message, 'content'):
                            response_text = last_message.content
                        else:
                            response_text = str(last_message)
                    else:
                        response_text = str(response)
                    
                    st.markdown(response_text)
                    
                    # Add assistant response to chat
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response_text
                    })
                    
                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })
else:
    st.info("👈 Please load documents from the sidebar to start chatting")
    
    # Show example
    st.markdown("### 🎯 How to use:")
    st.markdown("""
    1. **Choose your input method** in the sidebar:
       - Upload PDF files from your computer, or
       - Provide URLs to PDF documents
    2. **Load the documents** by clicking the button
    3. **Ask questions** about your documents in the chat
    
    ### 💡 Example questions:
    - "What is this document about?"
    - "Summarize the main points"
    - "Find information about [specific topic]"
    """)
