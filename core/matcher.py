from sentence_transformers import util
from sentence_transformers import SentenceTransformer

def match_resume_to_jd(resume_text: str, jd_text: str, embedding_model: SentenceTransformer) -> float:
    """Matches a resume to a job description and returns a similarity score.

    Args:
        resume_text: The text of the resume.
        jd_text: The text of the job description.
        embedding_model: The SentenceTransformer model to use for embeddings.

    Returns:
        A similarity score between 0 and 1.
    """
    resume_embedding = embedding_model.encode(resume_text, convert_to_tensor=True)
    jd_embedding = embedding_model.encode(jd_text, convert_to_tensor=True)

    cosine_scores = util.pytorch_cos_sim(resume_embedding, jd_embedding)
    return cosine_scores.item()
