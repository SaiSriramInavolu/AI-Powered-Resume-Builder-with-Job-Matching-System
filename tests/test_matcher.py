import unittest
from core.matcher import match_resume_to_jd

class TestMatcher(unittest.TestCase):

    def test_match_resume_to_jd(self):
        resume_text = "This is a resume."
        jd_text = "This is a job description."
        score = match_resume_to_jd(resume_text, jd_text)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 1)

if __name__ == '__main__':
    unittest.main()
