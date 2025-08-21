import unittest
from core.scorer import score_match

class TestScorer(unittest.TestCase):

    def test_score_match(self):
        resume_data = {
            'skills': ['Python', 'FastAPI', 'AWS'],
            'keywords': ['developer', 'engineer']
        }
        jd_data = {
            'skills': ['Python', 'FastAPI', 'AWS', 'Docker'],
            'keywords': ['developer', 'engineer', 'senior']
        }
        similarity_score = 0.8

        # Expected score calculation:
        # skill_score = 3/4 = 0.75
        # keyword_score = 2/3 = 0.666...
        # final_score = (0.5 * 0.75) + (0.3 * 0.8) + (0.2 * 0.666...)
        # final_score = 0.375 + 0.24 + 0.133... = 0.748...
        expected_score = (0.5 * 0.75) + (0.3 * 0.8) + (0.2 * (2/3))

        actual_score = score_match(resume_data, jd_data, similarity_score)

        self.assertAlmostEqual(actual_score, expected_score, places=2)

if __name__ == '__main__':
    unittest.main()