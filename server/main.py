import os
import joblib
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings.cohere import CohereEmbeddings
import cohere
from tenacity import retry, wait_exponential, stop_after_attempt
import time

# Flask app setup
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Replace with your Cohere API key
COHERE_API_KEY = "dnTP9WbkjF5EU8QRVYsOdrdbKwjzqAQk0pm4kiay"

# Initialize Cohere Embeddings
cohere_embeddings = CohereEmbeddings(
    cohere_api_key=COHERE_API_KEY,
    user_agent="gdpr-security-assessment"
)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@retry(wait=wait_exponential(multiplier=1, min=1, max=60), stop=stop_after_attempt(6))
def create_vectorstore_with_retry(texts, embeddings):
    try:
        return Chroma.from_documents(texts, embeddings)
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

def generate_response(query, docs):
    co = cohere.Client(COHERE_API_KEY)
    context = "\n".join([doc.page_content for doc in docs])
    prompt = f"Based on the following information:\n{context}\n\nAnswer the question: {query}"
    response = co.generate(
        model='command-xlarge-nightly',
        prompt=prompt,
        max_tokens=150,
        temperature=0.5
    )
    return response.generations[0].text.strip()

def assess_security_architecture(pdf_path):
    texts = process_pdf(pdf_path)
    vectorstore = process_texts_in_batches(texts, cohere_embeddings)

    security_aspects = [
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

    missing_aspects = []
    for aspect in security_aspects:
        query = f"Does the document mention or describe {aspect}?"
        docs = vectorstore.similarity_search(query)
        response = generate_response(query, docs)
        if "no" in response.lower() or "not mentioned" in response.lower():
            missing_aspects.append(aspect)

    return missing_aspects

def calculate_risk_score(missing_aspects):
    total_aspects = 10
    missing_count = len(missing_aspects)
    risk_score = (missing_count / total_aspects) * 100
    return risk_score

def get_aspect_details(aspect):
    details = {
        "Data minimization": {
            "description": "The practice of limiting the collection and retention of personal data to what is directly relevant and necessary for a specified purpose.",
            "threats": [
                "Excessive data collection leading to increased risk of data breaches",
                "Non-compliance with GDPR Article 5(1)(c) on data minimization",
                "Increased liability and potential fines due to unnecessary data retention"
            ],
            "recommendations": [
                "Implement data minimization techniques in all data collection processes",
                "Regularly review and purge unnecessary data",
                "Train staff on the importance of collecting only essential data"
            ]
        },
        "Incident response plan": {
            "description": "A documented, organized approach for addressing and managing the aftermath of a security breach or cyberattack.",
            "threats": [
                "Delayed or inadequate response to security incidents",
                "Increased damage and cost due to uncoordinated incident handling",
                "Potential non-compliance with GDPR's 72-hour breach notification requirement"
            ],
            "recommendations": [
                "Develop a comprehensive incident response plan",
                "Regularly test and update the plan through simulations",
                "Establish clear roles and responsibilities for incident response team members"
            ]
        },
        "Employee training": {
            "description": "Regular education of staff on data protection principles, security practices, and their responsibilities under GDPR.",
            "threats": [
                "Increased risk of human error leading to data breaches",
                "Lack of awareness about GDPR requirements among staff",
                "Potential mishandling of personal data due to ignorance"
            ],
            "recommendations": [
                "Implement a regular GDPR and data protection training program",
                "Conduct role-specific training for employees handling sensitive data",
                "Use real-world scenarios and interactive sessions to improve engagement"
            ]
        },
        "Third-party risk management": {
            "description": "The process of identifying, assessing, and controlling risks presented by relationships with external parties who process or have access to personal data.",
            "threats": [
                "Data breaches caused by insecure third-party practices",
                "Lack of visibility into data processing activities by third parties",
                "Non-compliance with GDPR due to inadequate third-party contracts"
            ],
            "recommendations": [
                "Conduct thorough due diligence on all third-party data processors",
                "Implement strong contractual safeguards with all third parties",
                "Regularly audit and review third-party compliance with GDPR requirements"
            ]
        }
    }
    return details.get(aspect, {})

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Process the uploaded PDF file
        missing_aspects = assess_security_architecture(file_path)
        risk_score = calculate_risk_score(missing_aspects)

        response = {
            "missing_aspects": missing_aspects,
            "risk_score": risk_score,
            "message": "Analysis complete",
            "details": {}
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