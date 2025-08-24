def score_match(resume_data: dict, jd_data: dict, similarity_score: float) -> float:
    """Scores the match between a resume and a job description.

    Args:
        resume_data: Parsed resume data (including skills and keywords).
        jd_data: Parsed job description data (including skills and keywords).
        similarity_score: The similarity score from the matcher.

    Returns:
        The final match score.
    """
    resume_skills = set(resume_data.get('skills', []))
    jd_skills = set(jd_data.get('skills', []))
    common_skills = resume_skills.intersection(jd_skills)
    skill_score = len(common_skills) / len(jd_skills) if jd_skills else 0

    resume_keywords = set(resume_data.get('keywords', []))
    jd_keywords = set(jd_data.get('keywords', []))
    common_keywords = resume_keywords.intersection(jd_keywords)
    keyword_score = len(common_keywords) / len(jd_keywords) if jd_keywords else 0

    # Weighted average: 50% skill score, 30% similarity score, 20% keyword score
    final_score = (0.5 * skill_score) + (0.3 * similarity_score) + (0.2 * keyword_score)

    return min(final_score, 1.0)