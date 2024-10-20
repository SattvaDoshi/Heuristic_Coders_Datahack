import os
import joblib
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings.cohere import CohereEmbeddings
import cohere
import time
from dotenv import load_dotenv



# Initialize Flask app
app = Flask(__name__)
load_dotenv()  # Load environment variables from .env file
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
# Cohere API Key and Configuration
cohere_embeddings = CohereEmbeddings(cohere_api_key=COHERE_API_KEY, user_agent="security-assessment")

# Define directories
UPLOAD_FOLDER = './uploads'
PERSIST_DIRECTORY = './chromadb_store'
TEXTS_FILE_PATH = './texts.pkl'

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Configure Flask to accept file uploads
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Maximum upload size: 16MB

# Function to process PDF and return split texts
def process_pdf(file_path):
    loader = PyPDFLoader(file_path)
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=50)
    texts = text_splitter.split_documents(data)
    return texts

# Function to create vector store from documents
def create_vectorstore_with_retry(texts, embeddings):
    return Chroma.from_documents(texts, embeddings)

# Function to generate Cohere response based on document search
def generate_response(query, docs, cohere_api_key):
    co = cohere.Client(cohere_api_key)
    context = "\n".join([doc.page_content for doc in docs])
    prompt = f"Based on the following information:\n{context}\n\nAnswer the question: {query}"
    response = co.generate(model='command-xlarge-nightly', prompt=prompt, max_tokens=150, temperature=0.5)
    return response.generations[0].text.strip()

# Function to dynamically generate questions based on security aspects
def generate_dynamic_questions(security_aspects):
    questions = []
    for aspect in security_aspects:
        questions.append(f"Does the document mention or describe {aspect}?")
    return questions

# Function to assess security aspects of a document
def assess_security_architecture(pdf_path):
    texts = process_pdf(pdf_path)
    vectorstore = create_vectorstore_with_retry(texts, cohere_embeddings)

    security_aspects = [
        "Data encryption", "Access control", "Data minimization", "Regular security audits",
        "Incident response plan", "Employee training", "Third-party risk management",
        "Data retention policies", "Privacy by design", "Consent management"
    ]

    missing_aspects = []
    questions = generate_dynamic_questions(security_aspects)
    for question in questions:
        docs = vectorstore.similarity_search(question)
        response = generate_response(question, docs, COHERE_API_KEY)
        if "no" in response.lower() or "not mentioned" in response.lower():
            missing_aspects.append(question)

    return missing_aspects, questions

# Function to calculate risk score
def calculate_risk_score(missing_aspects):
    total_aspects = 10
    missing_count = len(missing_aspects)
    risk_score = (missing_count / total_aspects) * 100
    return risk_score

# Endpoint to assess security aspects from a PDF and generate questions
@app.route('/assess', methods=['POST'])
def assess():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Assess the PDF and generate questions
        missing_aspects, questions = assess_security_architecture(file_path)
        risk_score = calculate_risk_score(missing_aspects)

        # Prepare the response
        response = {
            "questions": questions,
            "missing_aspects": missing_aspects,
            "risk_score": risk_score
        }
        return jsonify(response), 200

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
