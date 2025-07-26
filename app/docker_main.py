__import__('pysqlite3')
import sys
sys.modules["sqlite3"]=sys.modules.pop("pysqlite3")
import streamlit as st
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import Docx2txtLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts.chat import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain.document_loaders import Docx2txtLoader, PyPDFLoader
import tempfile
from dotenv import load_dotenv
import os
import shutil

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

embedding = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
llm = ChatOpenAI(api_key=OPENAI_API_KEY)


def load_vector_store(persist_dir="./chroma_db"):
    return Chroma(persist_directory=persist_dir, embedding_function=embedding)


chat_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        "You are a highly knowledgeable chat assistant. You must chat with users very politely. Use ONLY the provided context to answer the question.\n"
"If the answer is not in the context, reply: 'I don't know.' Think step by step when needed.\n\n"
"Context:\n{context}"
    ),
    HumanMessagePromptTemplate.from_template("{question}")
])


memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    input_key="question",
    output_key="answer" 
)

document_variable_name = "context" 
def build_qa_chain():
    db = load_vector_store()
    retriever = db.as_retriever(search_kwargs={"k": 5})
    print(chat_prompt)
    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": chat_prompt},
        return_source_documents=True,
        chain_type="stuff",  # or "refine", etc.
        output_key="answer" 
    )




from prometheus_client import Counter, Histogram, start_http_server, REGISTRY
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("chat_logger")

# Avoid double-registration
if "chat_requests_total" not in REGISTRY._names_to_collectors:
    REQUESTS = Counter("chat_requests_total", "Total number of user queries")
    LATENCY = Histogram("chat_response_latency_seconds", "Response time in seconds")
else:
    REQUESTS = REGISTRY._names_to_collectors["chat_requests_total"]
    LATENCY = REGISTRY._names_to_collectors["chat_response_latency_seconds"]

METRICS_STARTED = False

def start_metrics_server(port=9080):
    global METRICS_STARTED
    if not METRICS_STARTED:
        try:
            print(port)
            start_http_server(port)
            logger.info(f"Prometheus metrics server started on port {port}")
            METRICS_STARTED = True
        except Exception as e:
            logger.info("###############################")
            logger.warning(f"Metrics server already running on port: {port} {e}")


def observe_and_log(query, answer):
    start = time.time()
    REQUESTS.inc()
    logger.info(f"User query: {query}")
    logger.info(f"Model answer: {answer}")
    logger.info(f"latency: {time.time() - start}")
    LATENCY.observe(time.time() - start)

print("here")
start_metrics_server(8100)

print("#"*50)
st.title("RAG Chatbot with Memory + Role-based Prompt")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

qa_chain = build_qa_chain()

# Display chat history
if st.session_state.chat_history:
    st.markdown("### Chat History")
    for role, content in st.session_state.chat_history:
        if role == "user":
            st.markdown(f"**You:** {content}")
        else:
            st.markdown(f"**Bot:** {content}")


query = st.text_input("Ask something:")
with st.spinner("Thinking..."):
    if query:
        result = qa_chain({"question": query, "chat_history": st.session_state.chat_history})
        st.session_state.chat_history.append(("user", query))
        st.session_state.chat_history.append(("assistant", result["answer"]))
        st.write("### Answer:")
        st.write(result["answer"])
        observe_and_log(query, result["answer"])
print("#"*50)








