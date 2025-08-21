import unittest
from core.resume_parser import parse_pdf_resume

class TestResumeParser(unittest.TestCase):

    def test_parse_pdf_resume(self):
        with open('tests/temp/dummy_resume.pdf', 'rb') as f:
            parsed_resume = parse_pdf_resume(f)

        self.assertIsInstance(parsed_resume, dict)
        self.assertIn('text', parsed_resume)
        self.assertIn('skills', parsed_resume)
        self.assertIn('keywords', parsed_resume)

        # Note: The exact output of spaCy can vary slightly based on the model version.
        self.assertTrue(any(skill in parsed_resume['skills'] for skill in ['Google', 'AWS', 'Docker']))
        self.assertTrue(any(keyword in parsed_resume['keywords'] for keyword in ['Python', 'Developer', 'Engineer', 'Django', 'FastAPI']))

if __name__ == '__main__':
    unittest.main()