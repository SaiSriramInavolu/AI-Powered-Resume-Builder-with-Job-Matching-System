from pypdf import PdfReader
import spacy
from typing import IO

# Load spaCy model once
try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    print("Downloading spaCy model 'en_core_web_sm'...")
    spacy.cli.download('en_core_web_sm')
    nlp = spacy.load('en_core_web_sm')


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

    return parse_text_resume(text) # Reuse the text parsing logic


def parse_text_resume(text: str) -> dict:
    """Parses raw resume text to extract text, skills, and keywords.

    Args:
        text: The raw text content of the resume.

    Returns:
        A dictionary containing the extracted text, skills, and keywords.
    """
    doc = nlp(text)

    # Basic extraction for demonstration. You might want more sophisticated NER/parsing.
    skills = [ent.text for ent in doc.ents if ent.label_ in ['ORG', 'PRODUCT', 'GPE', 'NORP']] # Expanded entities for skills
    keywords = [token.text for token in doc if not token.is_stop and not token.is_punct and token.pos_ in ['NOUN', 'PROPN', 'ADJ']] # Expanded POS for keywords

    return {
        'text': text,
        'skills': list(set(skills)),
        'keywords': list(set(keywords))
    }