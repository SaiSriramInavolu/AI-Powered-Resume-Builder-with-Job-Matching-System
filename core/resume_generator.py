from io import BytesIO
from jinja2 import Environment, FileSystemLoader
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter



# ---------------- PDF Resume Builder ---------------- #
def create_pdf_resume(data: dict) -> BytesIO:
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=inch / 2,
        leftMargin=inch / 2,
        topMargin=inch / 2,
        bottomMargin=inch / 2,
    )
    styles = getSampleStyleSheet()

    # Create unique style names to avoid KeyError collisions with defaults
    styles.add(
        ParagraphStyle(
            name="MyHeading1",
            fontSize=28,
            leading=32,
            fontName="Times-Bold",
            alignment=TA_CENTER,
        )
    )
    styles.add(
        ParagraphStyle(
            name="MyHeading2",
            fontSize=16,
            leading=20,
            fontName="Times-Bold",
            alignment=TA_LEFT,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BodyTextSmall",
            fontSize=11,
            leading=14,
            fontName="Times-Roman",
            alignment=TA_LEFT,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BodyTextBullet",
            fontSize=11,
            leading=14,
            fontName="Times-Roman",
            alignment=TA_LEFT,
            leftIndent=20,
        )
    )
    styles.add(
        ParagraphStyle(
            name="ContactInfo",
            fontSize=11,
            leading=14,
            fontName="Times-Roman",
            alignment=TA_LEFT,
        )
    )

    story = []

    # Name and Contact Info
    story.append(Paragraph(data.get("name", "") or "", styles["MyHeading1"]))
    story.append(
        Paragraph(
            f"{data.get('email', '')} | {data.get('phone', '')}", styles["ContactInfo"]
        )
    )
    if data.get('github'):
        story.append(Paragraph(f"GitHub: <link href=\"{data['github']}\">{data['github']}</link>", styles["ContactInfo"]))
    if data.get('linkedin'):
        story.append(Paragraph(f"LinkedIn: <link href=\"{data['linkedin']}\">{data['linkedin']}</link>", styles["ContactInfo"]))
    story.append(Spacer(1, 0.2 * inch))

    # Summary
    if data.get("summary"):
        story.append(Paragraph("Summary", styles["MyHeading2"]))
        story.append(Paragraph(data["summary"], styles["BodyTextSmall"]))
        story.append(Spacer(1, 0.1 * inch))

    # Experience
    if data.get("experience"):
        story.append(Paragraph("Experience", styles["MyHeading2"]))
        for exp in data["experience"]:
            story.append(
                Paragraph(
                    f"<b>{exp.get('title', '')}</b> at {exp.get('company', '')} ({exp.get('years', '')})",
                    styles["BodyTextSmall"],
                )
            )
            if exp.get("description"):
                for line in (exp["description"] or "").split("\n"):
                    if line.strip():
                        story.append(Paragraph(line, styles["BodyTextBullet"]))
            story.append(Spacer(1, 0.05 * inch))
        story.append(Spacer(1, 0.1 * inch))

    # Education
    if data.get("education"):
        story.append(Paragraph("Education", styles["MyHeading2"]))
        for edu in data["education"]:
            story.append(
                Paragraph(
                    f"<b>{edu.get('degree', '')}</b>, {edu.get('university', '')} ({edu.get('graduation_year', '')})",
                    styles["BodyTextSmall"],
                )
            )
            if edu.get("description"):
                for line in (edu["description"] or "").split("\n"):
                    if line.strip():
                        story.append(Paragraph(line, styles["BodyTextBullet"]))
            story.append(Spacer(1, 0.05 * inch))
        story.append(Spacer(1, 0.1 * inch))

    # Projects
    if data.get("projects"):
        story.append(Paragraph("Projects", styles["MyHeading2"]))
        for proj in data["projects"]:
            story.append(Paragraph(f"<b>{proj.get('name', '')}</b>", styles["BodyTextSmall"]))
            if proj.get("technologies"):
                story.append(
                    Paragraph(
                        f"<i>Technologies:</i> {proj.get('technologies', '')}",
                        styles["BodyTextBullet"],
                    )
                )
            if proj.get("description"):
                for line in (proj["description"] or "").split("\n"):
                    if line.strip():
                        story.append(Paragraph(line, styles["BodyTextBullet"]))
            if proj.get("link"):
                story.append(
                    Paragraph(
                        f"Link: <font color='blue'>{proj.get('link', '')}</font>",
                        styles["BodyTextBullet"],
                    )
                )
            story.append(Spacer(1, 0.05 * inch))
        story.append(Spacer(1, 0.1 * inch))

    # Certifications
    if data.get("certifications"):
        story.append(Paragraph("Certifications", styles["MyHeading2"]))
        for cert in data["certifications"]:
            story.append(
                Paragraph(
                    f"<b>{cert.get('name', '')}</b> from {cert.get('organization', '')} ({cert.get('date_issued', '')})",
                    styles["BodyTextSmall"],
                )
            )
            story.append(Spacer(1, 0.05 * inch))
        story.append(Spacer(1, 0.1 * inch))

    # Skills
    if data.get("skills"):
        story.append(Paragraph("Skills", styles["MyHeading2"]))
        story.append(Paragraph(data["skills"], styles["BodyTextSmall"]))
        story.append(Spacer(1, 0.1 * inch))

    # Languages
    if data.get("languages"):
        story.append(Paragraph("Languages", styles["MyHeading2"]))
        for lang in data["languages"]:
            story.append(
                Paragraph(
                    f"{lang.get('language', '')} ({lang.get('proficiency', '')})",
                    styles["BodyTextSmall"],
                )
            )
            story.append(Spacer(1, 0.05 * inch))
        story.append(Spacer(1, 0.1 * inch))

    # Awards
    if data.get("awards"):
        story.append(Paragraph("Awards & Honors", styles["MyHeading2"]))
        for award in data["awards"]:
            story.append(
                Paragraph(
                    f"<b>{award.get('name', '')}</b> from {award.get('organization', '')} ({award.get('date', '')})",
                    styles["BodyTextSmall"],
                )
            )
            story.append(Spacer(1, 0.05 * inch))
        story.append(Spacer(1, 0.1 * inch))

    doc.build(story)
    buffer.seek(0)
    return buffer




import os
import json
import google.generativeai as genai
from langchain_core.pydantic_v1 import BaseModel, Field  # Keep BaseModel for schema definition

# Define Pydantic models for structured output
class Experience(BaseModel):
    title: str = Field(description="Job title")
    company: str = Field(description="Company name")
    years: str = Field(description="Years worked (e.g., 2020-2023)")
    description: list[str] = Field(description="List of bullet points describing responsibilities and achievements")

class Education(BaseModel):
    degree: str = Field(description="Degree obtained")
    university: str = Field(description="University name")
    graduation_year: str = Field(description="Graduation year")
    description: list[str] = Field(description="List of bullet points describing academic achievements or coursework")

class Project(BaseModel):
    name: str = Field(description="Project name")
    technologies: str = Field(description="Technologies used (comma-separated)")
    description: list[str] = Field(description="List of bullet points describing the project and its impact")
    link: str = Field(description="Link to the project (optional)")

class Certification(BaseModel):
    name: str = Field(description="Certification name")
    organization: str = Field(description="Issuing organization")
    date_issued: str = Field(description="Date issued (e.g., Month Year)")

class Language(BaseModel):
    language: str = Field(description="Language name")
    proficiency: str = Field(description="Proficiency level (e.g., Native, Fluent, Conversational)")

class Award(BaseModel):
    name: str = Field(description="Award name")
    organization: str = Field(description="Awarding organization")
    date: str = Field(description="Date received (e.g., Month Year)")

class ResumeData(BaseModel):
    name: str = Field(description="Full name")
    email: str = Field(description="Email address")
    phone: str = Field(description="Phone number")
    linkedin: str = Field(description="LinkedIn profile URL")
    github: str = Field(description="GitHub profile URL")
    summary: str = Field(description="Professional summary or objective")
    experience: list[Experience] = Field(description="List of work experiences")
    education: list[Education] = Field(description="List of educational backgrounds")
    projects: list[Project] = Field(description="List of personal or professional projects")
    skills: str = Field(description="Comma-separated list of technical and soft skills")
    certifications: list[Certification] = Field(description="List of certifications")
    languages: list[Language] = Field(description="List of languages and proficiency levels")
    awards: list[Award] = Field(description="List of awards and honors")


class ResumeGenerator:
    def __init__(self):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel('gemini-pro')
        self.resume_data_schema = ResumeData.schema_json(indent=2)

    def generate_resume_content_with_gemini(self, user_input: str) -> dict:
        prompt_template = f"""Generate comprehensive resume data based on the following user input.
            Format the output as a JSON object strictly adhering to the provided schema.
            Ensure all fields are populated with realistic and detailed information.
            If a field is not explicitly mentioned in the input, generate plausible content for it.

            User Input: {user_input}

            JSON Schema:
            {self.resume_data_schema}
            """
        try:
            response = self.model.generate_content(prompt_template)
            # Assuming the model returns a JSON string in its text attribute
            resume_data = json.loads(response.text)
            return resume_data
        except Exception as e:
            print(f"Error generating resume content with Gemini: {e}")
            return {}

    def generate_resume(self, resume_data: dict, output_format: str = "pdf") -> BytesIO:
        if output_format == "pdf":
            return create_pdf_resume(resume_data)
        else:
            raise ValueError("Unsupported output format. Choose 'pdf'.")