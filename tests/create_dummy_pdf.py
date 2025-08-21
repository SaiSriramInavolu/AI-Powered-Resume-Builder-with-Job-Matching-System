import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_dummy_pdf(file_path: str, text: str):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    c = canvas.Canvas(file_path, pagesize=letter)
    text_object = c.beginText(100, 750)
    for line in text.split('\n'):
        text_object.textLine(line)
    c.drawText(text_object)
    c.save()

if __name__ == '__main__':
    resume_text = (
        "John Doe\n"
        "Python Developer\n\n"
        "Experience:\n"
        "- Software Engineer at Google (2020-Present)\n"
        "- Developed and maintained web applications using Python, Django, and FastAPI.\n"
        "- Worked with AWS and Docker for deployment.\n\n"
        "Skills:\n"
        "- Python, Django, FastAPI, JavaScript, React\n"
        "- AWS, Docker, Kubernetes\n"
    )
    create_dummy_pdf('tests/temp/dummy_resume.pdf', resume_text)