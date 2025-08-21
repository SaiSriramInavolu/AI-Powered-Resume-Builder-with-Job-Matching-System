from sentence_transformers import SentenceTransformer, util

def match_resume_to_jd(resume_text: str, jd_text: str) -> float:
    """Matches a resume to a job description and returns a similarity score.

    Args:
        resume_text: The text of the resume.
        jd_text: The text of the job description.

    Returns:
        A similarity score between 0 and 1.
    """
    model = SentenceTransformer('all-MiniLM-L6-v2')
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
    jd_embedding = model.encode(jd_text, convert_to_tensor=True)

    cosine_scores = util.pytorch_cos_sim(resume_embedding, jd_embedding)
    return cosine_scores.item()
