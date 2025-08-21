import unittest
from core.jd_parser import parse_text_job_description

class TestJdParser(unittest.TestCase):

    def test_parse_text_job_description(self):
        jd_text = "We are looking for a Python developer with experience in FastAPI and AWS. Knowledge of Docker is a plus."
        parsed_jd = parse_text_job_description(jd_text)

        self.assertIsInstance(parsed_jd, dict)
        self.assertIn('skills', parsed_jd)
        self.assertIn('keywords', parsed_jd)

        # Note: The exact output of spaCy can vary slightly based on the model version.
        # This test is designed to be flexible.
        self.assertTrue(any(skill in parsed_jd['skills'] for skill in ['FastAPI', 'AWS', 'Docker']))
        self.assertTrue(any(keyword in parsed_jd['keywords'] for keyword in ['Python', 'developer', 'experience', 'Knowledge']))

if __name__ == '__main__':
    unittest.main()