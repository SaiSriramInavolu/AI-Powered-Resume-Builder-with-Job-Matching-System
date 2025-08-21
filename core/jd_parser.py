import spacy

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

    return {
        'text': text,
        'skills': list(set(skills)),
        'keywords': list(set(keywords))
    }
