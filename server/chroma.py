import os
import joblib
import time
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings.cohere import CohereEmbeddings
from tenacity import retry, wait_exponential, stop_after_attempt

# Replace with your Cohere API key
COHERE_API_KEY = "Zd3gb7sVtS9sp6chWG010MQHOiMSUinLW10LHyX1"

# Initialize Cohere Embeddings
cohere_embeddings = CohereEmbeddings(
    cohere_api_key=COHERE_API_KEY,
    user_agent="security-assessment"
)

# Define paths
persist_directory = "./chromadb_store"
texts_file_path = "./texts.pkl"

@retry(wait=wait_exponential(multiplier=1, min=1, max=60), stop=stop_after_attempt(6))
def create_vectorstore_with_retry(texts, embeddings):
    try:
        return Chroma.from_documents(texts, embeddings, persist_directory=persist_directory)
    except Exception as e:
        if "Rate limit" in str(e):
            print("Rate limit hit. Retrying...")
            raise
        else:
            raise

def process_pdf(file_path):
    loader = PyPDFLoader(file_path)
    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=50)
    texts = text_splitter.split_documents(data)

    # Save texts locally to avoid re-processing
    joblib.dump(texts, texts_file_path)
    return texts

def process_texts_in_batches(texts, embeddings, batch_size=150, delay=5):
    vectorstore = None
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        vectorstore = create_vectorstore_with_retry(batch, embeddings)
        vectorstore.persist()
        print(f"Processed batch {i // batch_size + 1}")
        time.sleep(delay)
    return vectorstore

# Example usage
if __name__ == "__main__":
    pdf_path = "D:\Web development\Hackathon\DataHack\Heuristic_Coders_Datahack\server\ilovepdf_merged.pdf"
    
    if not os.path.exists(texts_file_path):
        texts = process_pdf(pdf_path)
    else:
        texts = joblib.load(texts_file_path)
    
    vectorstore = process_texts_in_batches(texts, cohere_embeddings)
    print("ChromaDB setup complete.")
