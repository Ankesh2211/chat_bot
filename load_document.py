from langchain.document_loaders import Docx2txtLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
import os
import argparse
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

embedding = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
def load_documents(path):
    if path.endswith("pdf"):
        loader = PyPDFLoader(path)
    elif path.endswith("docx"):
        loader = Docx2txtLoader(path)
    else:
        raise ValueError("Unsupported file format. Use .pdf or .docx")
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=300)
    return splitter.split_documents(documents)

def store_embeddings(docs, persist_dir="./chroma_db"):
    db = Chroma.from_documents(docs, embedding, persist_directory=persist_dir)
    db.persist()
    return db

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Take user input via CLI")
    parser.add_argument("--path", type=str, required=True, help="Your name")
    args = parser.parse_args()
    path = args.path
    docs = load_documents(path)
    store_embeddings(docs)