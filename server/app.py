import os
from typing import List, Dict, Any
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings.cohere import CohereEmbeddings
from langchain.prompts import PromptTemplate
from langchain.llms import Cohere
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
import cohere
from tenacity import retry, wait_exponential, stop_after_attempt
import time
import json

# Flask app setup
app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
COHERE_API_KEY = "dnTP9WbkjF5EU8QRVYsOdrdbKwjzqAQk0pm4kiay"
BATCH_SIZE = 150
DELAY = 5

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize Cohere Embeddings and LLM
cohere_embeddings = CohereEmbeddings(cohere_api_key=COHERE_API_KEY, user_agent="gdpr-security-assessment")
cohere_llm = Cohere(cohere_api_key=COHERE_API_KEY)

# Security aspects
SECURITY_ASPECTS = [
    "Data encryption",
    "Access control",
    "Data minimization",
    "Regular security audits",
    "Incident response plan",
    "Employee training",
    "Third-party risk management",
    "Data retention policies",
    "Privacy by design",
    "Consent management"
]

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@retry(wait=wait_exponential(multiplier=1, min=1, max=60), stop=stop_after_attempt(6))
def create_vectorstore_with_retry(texts: List[Any], embeddings: Any) -> Chroma:
    try:
        return Chroma.from_documents(texts, embeddings)
    except Exception as e:
        if "Rate limit" in str(e):
            print("Rate limit hit. Retrying...")
            raise
        else:
            raise

def process_pdf(file_path: str) -> List[Any]:
    loader = PyPDFLoader(file_path)
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=50)
    return text_splitter.split_documents(data)

def process_texts_in_batches(texts: List[Any], embeddings: Any) -> Chroma:
    vectorstore = None
    for i in range(0, len(texts), BATCH_SIZE):
        batch = texts[i:i + BATCH_SIZE]
        vectorstore = create_vectorstore_with_retry(batch, embeddings)
        print(f"Processed batch {i // BATCH_SIZE + 1}")
        time.sleep(DELAY)
    return vectorstore

def generate_response(query: str, docs: List[Any]) -> str:
    context = "\n".join([doc.page_content for doc in docs])
    prompt = PromptTemplate(
        input_variables=["context", "query"],
        template="Based on the following information:\n{context}\n\nAnswer the question: {query}"
    )
    chain = (
        {"context": RunnablePassthrough(), "query": RunnablePassthrough()}
        | prompt
        | cohere_llm
        | StrOutputParser()
    )
    return chain.invoke({"context": context, "query": query})

def assess_security_architecture(pdf_path: str) -> List[str]:
    texts = process_pdf(pdf_path)
    vectorstore = process_texts_in_batches(texts, cohere_embeddings)

    missing_aspects = []
    for aspect in SECURITY_ASPECTS:
        query = f"Does the document mention or describe {aspect}? Provide a detailed explanation."
        docs = vectorstore.similarity_search(query)
        response = generate_response(query, docs)
        if "no" in response.lower() or "not mentioned" in response.lower():
            missing_aspects.append(aspect)

    return missing_aspects

def calculate_risk_score(missing_aspects: List[str]) -> float:
    return (len(missing_aspects) / len(SECURITY_ASPECTS)) * 100

def get_aspect_details(aspect: str) -> Dict[str, Any]:
    prompt = PromptTemplate(
        input_variables=["aspect"],
        template="Provide a detailed analysis of the security aspect: {aspect}. Include a description, potential threats, and specific recommendations."
    )
    chain = prompt | cohere_llm | StrOutputParser()
    response = chain.invoke({"aspect": aspect})
    
    try:
        details = json.loads(response)
    except json.JSONDecodeError:
        # Fallback to a simple structure if JSON parsing fails
        details = {
            "description": response[:200],
            "threats": [response[200:400]],
            "recommendations": [response[400:600]]
        }
    
    return details

def generate_custom_recommendations(missing_aspects: List[str], company_info: Dict[str, Any]) -> str:
    aspects_str = ", ".join(missing_aspects)
    prompt = PromptTemplate(
        input_variables=["aspects", "company_info"],
        template="Based on the missing security aspects ({aspects}) and the following company information:\n{company_info}\n\nProvide detailed, customized recommendations for improving the company's security posture."
    )
    chain = prompt | cohere_llm | StrOutputParser()
    return chain.invoke({"aspects": aspects_str, "company_info": json.dumps(company_info)})

def generate_executive_summary(risk_score: float, missing_aspects: List[str], company_info: Dict[str, Any]) -> str:
    aspects_str = ", ".join(missing_aspects)
    prompt = PromptTemplate(
        input_variables=["risk_score", "aspects", "company_info"],
        template="Generate an executive summary for a security assessment report. Risk score: {risk_score}%, Missing aspects: {aspects}. Company info: {company_info}"
    )
    chain = prompt | cohere_llm | StrOutputParser()
    return chain.invoke({"risk_score": risk_score, "aspects": aspects_str, "company_info": json.dumps(company_info)})

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    company_info = request.form.get('company_info', '{}')
    try:
        company_info = json.loads(company_info)
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid company info format"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        missing_aspects = assess_security_architecture(file_path)
        risk_score = calculate_risk_score(missing_aspects)

        response = {
            "missing_aspects": missing_aspects,
            "risk_score": risk_score,
            "message": "Analysis complete",
            "details": {},
            "custom_recommendations": generate_custom_recommendations(missing_aspects, company_info),
            "executive_summary": generate_executive_summary(risk_score, missing_aspects, company_info)
        }

        if risk_score < 20:
            response["risk_level"] = "Low risk: Your security architecture is robust."
        elif risk_score < 50:
            response["risk_level"] = "Medium risk: There are some gaps in your security architecture that should be addressed."
        else:
            response["risk_level"] = "High risk: Significant improvements are needed in your security architecture."

        for aspect in missing_aspects:
            response["details"][aspect] = get_aspect_details(aspect)

        return jsonify(response)
    else:
        return jsonify({"error": "File type not allowed"}), 400

if __name__ == '__main__':
    app.run(debug=True)