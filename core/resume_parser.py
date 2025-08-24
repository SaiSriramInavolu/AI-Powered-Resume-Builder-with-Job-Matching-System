import hashlib
from pypdf import PdfReader
import spacy
from typing import IO

from core.vector_db import VectorDB

# Load spaCy model once
try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    print("Downloading spaCy model 'en_core_web_sm'...")
    spacy.cli.download('en_core_web_sm')
    nlp = spacy.load('en_core_web_sm')

# Initialize VectorDB
vector_db = VectorDB()

def parse_pdf_resume(file: IO[bytes]) -> dict:
    """Parses a PDF resume to extract text, skills, and keywords.

    Args:
        file: A file-like object representing the PDF resume.

    Returns:
        A dictionary containing the extracted text, skills, and keywords.
    """
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    return parse_text_resume(text) 


def parse_text_resume(text: str) -> dict:
    """Parses raw resume text to extract text, skills, and keywords.

    Args:
        text: The raw text content of the resume.

    Returns:
        A dictionary containing the extracted text, skills, and keywords.
    """
    doc = nlp(text)

    skills = [ent.text for ent in doc.ents if ent.label_ in ['ORG', 'PRODUCT', 'GPE', 'NORP']] 
    keywords = [token.text for token in doc if not token.is_stop and not token.is_punct and token.pos_ in ['NOUN', 'PROPN', 'ADJ']] 
    parsed_data = {
        'text': text,
        'skills': list(set(skills)),
        'keywords': list(set(keywords))
    }

    
    document_id = hashlib.sha256(text.encode()).hexdigest()
    combined_text = f"""Skills: {", ".join(parsed_data["skills"])}. Keywords: {", ".join(parsed_data["keywords"])}. {parsed_data["text"]}"""
    vector_db.add_document(document_id, combined_text, {"type": "resume", "id": document_id})

    return parsed_data