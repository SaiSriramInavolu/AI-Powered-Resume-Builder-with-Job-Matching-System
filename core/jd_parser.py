import spacy
import hashlib
from core.vector_db import VectorDB

vector_db = VectorDB()

def parse_text_job_description(text: str) -> dict:
    """Parses a text job description using spaCy to extract named entities and keywords.

    Args:
        text: The job description text.

    Returns:
        A dictionary containing the extracted skills, keywords and the original text.
    """ 
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)

    skills = [ent.text for ent in doc.ents if ent.label_ in ['ORG', 'PRODUCT']]
    keywords = [token.text for token in doc if not token.is_stop and not token.is_punct and token.pos_ in ['NOUN', 'PROPN']]

    parsed_data = {
        'text': text,
        'skills': list(set(skills)),
        'keywords': list(set(keywords))
    }

    
    document_id = hashlib.sha256(text.encode()).hexdigest()
    combined_text = f"""Skills: {", ".join(parsed_data["skills"])}. Keywords: {", ".join(parsed_data["keywords"])}. {parsed_data["text"]}"""
    vector_db.add_document(document_id, combined_text, {"type": "job_description", "id": document_id})

    return parsed_data
