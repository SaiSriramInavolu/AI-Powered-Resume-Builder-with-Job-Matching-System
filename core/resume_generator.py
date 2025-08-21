# from io import BytesIO
# from jinja2 import Environment, FileSystemLoader
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib.enums import TA_LEFT, TA_CENTER
# from reportlab.lib.units import inch, letter
# env = Environment(
#     loader=FileSystemLoader('.'),
#     block_start_string='((%',
#     block_end_string='%))',
#     variable_start_string='(((',
#     variable_end_string=')))',
#     comment_start_string='((#',
#     comment_end_string='#))',
# )

# # ---------------- PDF Resume Builder ---------------- #
# def create_pdf_resume(data: dict) -> BytesIO:
#     buffer = BytesIO()
#     doc = SimpleDocTemplate(
#         buffer,
#         pagesize=letter,
#         rightMargin=inch / 2,
#         leftMargin=inch / 2,
#         topMargin=inch / 2,
#         bottomMargin=inch / 2,
#     )
#     styles = getSampleStyleSheet()

#     # Create unique style names to avoid KeyError collisions with defaults
#     styles.add(
#         ParagraphStyle(
#             name="MyHeading1",
#             fontSize=28,
#             leading=32,
#             fontName="Times-Bold",
#             alignment=TA_CENTER,
#         )
#     )
#     styles.add(
#         ParagraphStyle(
#             name="MyHeading2",
#             fontSize=16,
#             leading=20,
#             fontName="Times-Bold",
#             alignment=TA_LEFT,
#         )
#     )
#     styles.add(
#         ParagraphStyle(
#             name="BodyTextSmall",
#             fontSize=11,
#             leading=14,
#             fontName="Times-Roman",
#             alignment=TA_LEFT,
#         )
#     )
#     styles.add(
#         ParagraphStyle(
#             name="BodyTextBullet",
#             fontSize=11,
#             leading=14,
#             fontName="Times-Roman",
#             alignment=TA_LEFT,
#             leftIndent=20,
#         )
#     )
#     styles.add(
#         ParagraphStyle(
#             name="ContactInfo",
#             fontSize=11,
#             leading=14,
#             fontName="Times-Roman",
#             alignment=TA_LEFT,
#         )
#     )

#     story = []

#     # Name and Contact Info
#     story.append(Paragraph(data.get("name", "") or "", styles["MyHeading1"]))
#     story.append(
#         Paragraph(
#             f"{data.get('email', '')} | {data.get('phone', '')}", styles["ContactInfo"]
#         )
#     )
#     if data.get('github'):
#         story.append(Paragraph(f"GitHub: <link href=\"{data['github']}\">{data['github']}</link>", styles["ContactInfo"]))
#     if data.get('linkedin'):
#         story.append(Paragraph(f"LinkedIn: <link href=\"{data['linkedin']}\">{data['linkedin']}</link>", styles["ContactInfo"]))
#     story.append(Spacer(1, 0.2 * inch))

#     # Summary
#     if data.get("summary"):
#         story.append(Paragraph("Summary", styles["MyHeading2"]))
#         story.append(Paragraph(data["summary"], styles["BodyTextSmall"]))
#         story.append(Spacer(1, 0.1 * inch))

#     # Experience
#     if data.get("experience"):
#         story.append(Paragraph("Experience", styles["MyHeading2"]))
#         for exp in data["experience"]:
#             story.append(
#                 Paragraph(
#                     f"<b>{exp.get('title', '')}</b> at {exp.get('company', '')} ({exp.get('years', '')})",
#                     styles["BodyTextSmall"],
#                 )
#             )
#             if exp.get("description"):
#                 for line in (exp["description"] or "").split("\n"):
#                     if line.strip():
#                         story.append(Paragraph(line, styles["BodyTextBullet"]))
#             story.append(Spacer(1, 0.05 * inch))
#         story.append(Spacer(1, 0.1 * inch))

#     # Education
#     if data.get("education"):
#         story.append(Paragraph("Education", styles["MyHeading2"]))
#         for edu in data["education"]:
#             story.append(
#                 Paragraph(
#                     f"<b>{edu.get('degree', '')}</b>, {edu.get('university', '')} ({edu.get('graduation_year', '')})",
#                     styles["BodyTextSmall"],
#                 )
#             )
#             if edu.get("description"):
#                 for line in (edu["description"] or "").split("\n"):
#                     if line.strip():
#                         story.append(Paragraph(line, styles["BodyTextBullet"]))
#             story.append(Spacer(1, 0.05 * inch))
#         story.append(Spacer(1, 0.1 * inch))

#     # Projects
#     if data.get("projects"):
#         story.append(Paragraph("Projects", styles["MyHeading2"]))
#         for proj in data["projects"]:
#             story.append(Paragraph(f"<b>{proj.get('name', '')}</b>", styles["BodyTextSmall"]))
#             if proj.get("technologies"):
#                 story.append(
#                     Paragraph(
#                         f"<i>Technologies:</i> {proj.get('technologies', '')}",
#                         styles["BodyTextBullet"],
#                     )
#                 )
#             if proj.get("description"):
#                 for line in (proj["description"] or "").split("\n"):
#                     if line.strip():
#                         story.append(Paragraph(line, styles["BodyTextBullet"]))
#             if proj.get("link"):
#                 story.append(
#                     Paragraph(
#                         f"Link: <font color='blue'>{proj.get('link', '')}</font>",
#                         styles["BodyTextBullet"],
#                     )
#                 )
#             story.append(Spacer(1, 0.05 * inch))
#         story.append(Spacer(1, 0.1 * inch))

#     # Certifications
#     if data.get("certifications"):
#         story.append(Paragraph("Certifications", styles["MyHeading2"]))
#         for cert in data["certifications"]:
#             story.append(
#                 Paragraph(
#                     f"<b>{cert.get('name', '')}</b> from {cert.get('organization', '')} ({cert.get('date_issued', '')})",
#                     styles["BodyTextSmall"],
#                 )
#             )
#             story.append(Spacer(1, 0.05 * inch))
#         story.append(Spacer(1, 0.1 * inch))

#     # Skills
#     if data.get("skills"):
#         story.append(Paragraph("Skills", styles["MyHeading2"]))
#         story.append(Paragraph(data["skills"], styles["BodyTextSmall"]))
#         story.append(Spacer(1, 0.1 * inch))

#     # Languages
#     if data.get("languages"):
#         story.append(Paragraph("Languages", styles["MyHeading2"]))
#         for lang in data["languages"]:
#             story.append(
#                 Paragraph(
#                     f"{lang.get('language', '')} ({lang.get('proficiency', '')})",
#                     styles["BodyTextSmall"],
#                 )
#             )
#             story.append(Spacer(1, 0.05 * inch))
#         story.append(Spacer(1, 0.1 * inch))

#     # Awards
#     if data.get("awards"):
#         story.append(Paragraph("Awards & Honors", styles["MyHeading2"]))
#         for award in data["awards"]:
#             story.append(
#                 Paragraph(
#                     f"<b>{award.get('name', '')}</b> from {award.get('organization', '')} ({award.get('date', '')})",
#                     styles["BodyTextSmall"],
#                 )
#             )
#             story.append(Spacer(1, 0.05 * inch))
#         story.append(Spacer(1, 0.1 * inch))

#     doc.build(story)
#     buffer.seek(0)
#     return buffer


# # ---------------- LaTeX Resume Builder ---------------- #
# def create_latex_resume(data: dict) -> str:
#     def escape_latex(text):
#         if not text:
#             return ""
#         return (
#             text.replace("&", r"\\&")
#             .replace("%", r"\\%")
#             .replace("$", r"\\$")
#             .replace("#", r"\\#")
#             .replace("_", r"\\_")
#             .replace("{", r"\\{")
#             .replace("}", r"\\}")
#             .replace("~", r"\\textasciitilde{}")
#             .replace("^", r"\\textasciicircum{}")
            
#         )

#     name = escape_latex(data.get("name", ""))
#     email = escape_latex(data.get("email", ""))
#     phone = escape_latex(data.get("phone", ""))
#     github_url = escape_latex(data.get("github", ""))
#     linkedin_url = escape_latex(data.get("linkedin", ""))
#     summary = escape_latex(data.get("summary", ""))
#     skills = escape_latex(data.get("skills", ""))

#     experience_latex = ""
#     for exp in data.get("experience", []):
#         title = escape_latex(exp.get("title", ""))
#         company = escape_latex(exp.get("company", ""))
#         years = escape_latex(exp.get("years", ""))
#         description = escape_latex(exp.get("description", "")).replace("\n", r"\\\\")
#         experience_latex += f"\textbf{{{title}}} at \textit{{{company}}} ({years})\\"
#         if description:
#             experience_latex += f"{description}\\\vspace{{0.1cm}}\n"

#     education_latex = ""
#     for edu in data.get("education", []):
#         degree = escape_latex(edu.get("degree", ""))
#         university = escape_latex(edu.get("university", ""))
#         graduation_year = escape_latex(edu.get("graduation_year", ""))
#         description = escape_latex(edu.get("description", "")).replace("\n", r"\\\\")
#         education_latex += f"\textbf{{{degree}}}, \textit{{{university}}} ({graduation_year})\\"
#         if description:
#             education_latex += f"{description}\\\vspace{{0.1cm}}\n"

#     projects_latex = ""
#     for proj in data.get("projects", []):
#         proj_name = escape_latex(proj.get("name", ""))
#         technologies = escape_latex(proj.get("technologies", ""))
#         description = escape_latex(proj.get("description", "")).replace("\n", r"\\\\")
#         link = escape_latex(proj.get("link", ""))
#         projects_latex += f"\textbf{{{proj_name}}}\\\""
#         if technologies:
#             projects_latex += f"\textit{{Technologies:}} {technologies}\\\""
#         if description:
#             projects_latex += f"{description}\\\""
#         if link:
#             projects_latex += f"Link: \url{{{link}}}\\\""
#         projects_latex += "\vspace{0.1cm}\n"

#     certifications_latex = ""
#     for cert in data.get("certifications", []):
#         cert_name = escape_latex(cert.get("name", ""))
#         organization = escape_latex(cert.get("organization", ""))
#         date_issued = escape_latex(cert.get("date_issued", ""))
#         certifications_latex += (
#             f"\textbf{{{cert_name}}} from {organization} ({date_issued})\\"
#         )
#         certifications_latex += "\vspace{0.1cm}\n"

#     languages_latex = ""
#     for lang in data.get("languages", []):
#         language = escape_latex(lang.get("language", ""))
#         proficiency = escape_latex(lang.get("proficiency", ""))
#         languages_latex += f"{language} (\textit{{{proficiency}}})\\"
#         languages_latex += "\vspace{0.1cm}\n"

#     awards_latex = ""
#     for award in data.get("awards", []):
#         award_name = escape_latex(award.get("name", ""))
#         organization = escape_latex(award.get("organization", ""))
#         date = escape_latex(award.get("date", ""))
#         awards_latex += f"\textbf{{{award_name}}} from {organization} ({date})\\"
#         awards_latex += "\vspace{0.1cm}\\n"

#     latex_content = fr"""
# \documentclass[10pt, a4paper]{{article}}
# \usepackage[utf8]{{inputenc}}
# \usepackage[T1]{{fontenc}}
# \usepackage{{geometry}}
# \geometry{{left=1in, right=1in, top=1in, bottom=1in}}
# \usepackage{{enumitem}}
# \setlist[itemize]{{noitemsep, topsep=0pt, parsep=0pt, partopsep=0pt}}
# \usepackage{{hyperref}}
# \hypersetup{{
#     colorlinks=true,
#     urlcolor=blue,
# }}
# \usepackage{{helvet}} % Use Helvetica font
# \renewcommand{{\familydefault}}{{\sfdefault}} % Set sans-serif as default font

# \begin{{document}}

# \begin{{center}}
#     {{\fontsize{{28pt}}{{32pt}}\selectfont \textbf{{{name}}}}}\\
#     \[5pt] % Add some vertical space
#     {{\fontsize{{11pt}}{{14pt}}\selectfont {email} $|$ {phone}}}
#     \[2pt] % Add some vertical space
#     {{\fontsize{{11pt}}{{14pt}}\selectfont \href{{{github_url}}}{{GitHub}} $|$ \href{{{linkedin_url}}}{{LinkedIn}}}}
# \end{{center}}

# \section*{\fontsize{{16pt}}{{20pt}}\selectfont Summary}
# {summary}

# \section*{\fontsize{{16pt}}{{20pt}}\selectfont Experience}
# {experience_latex}

# \section*{\fontsize{{16pt}}{{20pt}}\selectfont Education}
# {education_latex}

# \section*{\fontsize{{16pt}}{{20pt}}\selectfont Projects}
# {projects_latex}

# \section*{\fontsize{{16pt}}{{20pt}}\selectfont Skills}
# {skills}

# \section*{\fontsize{{16pt}}{{20pt}}\selectfont Certifications}
# {certifications_latex}

# \section*{\fontsize{{16pt}}{{20pt}}\selectfont Languages}
# {languages_latex}

# \section*{\fontsize{{16pt}}{{20pt}}\selectfont Awards & Honors}
# {awards_latex}

# \end{{document}}
# """
#     return latex_content

# import os
# import json
# import google.generativeai as genai
# from langchain_core.pydantic_v1 import BaseModel, Field # Keep BaseModel for schema definition

# # Define Pydantic models for structured output
# class Experience(BaseModel):
#     title: str = Field(description="Job title")
#     company: str = Field(description="Company name")
#     years: str = Field(description="Years worked (e.g., 2020-2023)")
#     description: list[str] = Field(description="List of bullet points describing responsibilities and achievements")

# class Education(BaseModel):
#     degree: str = Field(description="Degree obtained")
#     university: str = Field(description="University name")
#     graduation_year: str = Field(description="Graduation year")
#     description: list[str] = Field(description="List of bullet points describing academic achievements or coursework")

# class Project(BaseModel):
#     name: str = Field(description="Project name")
#     technologies: str = Field(description="Technologies used (comma-separated)")
#     description: list[str] = Field(description="List of bullet points describing the project and its impact")
#     link: str = Field(description="Link to the project (optional)")

# class Certification(BaseModel):
#     name: str = Field(description="Certification name")
#     organization: str = Field(description="Issuing organization")
#     date_issued: str = Field(description="Date issued (e.g., Month Year)")

# class Language(BaseModel):
#     language: str = Field(description="Language name")
#     proficiency: str = Field(description="Proficiency level (e.g., Native, Fluent, Conversational)")

# class Award(BaseModel):
#     name: str = Field(description="Award name")
#     organization: str = Field(description="Awarding organization")
#     date: str = Field(description="Date received (e.g., Month Year)")

# class ResumeData(BaseModel):
#     name: str = Field(description="Full name")
#     email: str = Field(description="Email address")
#     phone: str = Field(description="Phone number")
#     linkedin: str = Field(description="LinkedIn profile URL")
#     github: str = Field(description="GitHub profile URL")
#     summary: str = Field(description="Professional summary or objective")
#     experience: list[Experience] = Field(description="List of work experiences")
#     education: list[Education] = Field(description="List of educational backgrounds")
#     projects: list[Project] = Field(description="List of personal or professional projects")
#     skills: str = Field(description="Comma-separated list of technical and soft skills")
#     certifications: list[Certification] = Field(description="List of certifications")
#     languages: list[Language] = Field(description="List of languages and proficiency levels")
#     awards: list[Award] = Field(description="List of awards and honors")


# class ResumeGenerator:
#     def __init__(self):
#         genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
#         self.model = genai.GenerativeModel('gemini-pro')
#         self.resume_data_schema = ResumeData.schema_json(indent=2)

#     def generate_resume_content_with_gemini(self, user_input: str) -> dict:
#         prompt_template = f"""Generate comprehensive resume data based on the following user input.
#             Format the output as a JSON object strictly adhering to the provided schema.
#             Ensure all fields are populated with realistic and detailed information.
#             If a field is not explicitly mentioned in the input, generate plausible content for it.

#             User Input: {user_input}

#             JSON Schema:
#             {self.resume_data_schema}
#             """
#         try:
#             response = self.model.generate_content(prompt_template)
#             # Assuming the model returns a JSON string in its text attribute
#             resume_data = json.loads(response.text)
#             return resume_data
#         except Exception as e:
#             print(f"Error generating resume content with Gemini: {e}")
#             return {{}}

#     def generate_resume(self, resume_data: dict, output_format: str = "latex") -> str | BytesIO:
#         if output_format == "latex":
#             return create_latex_resume(resume_data)
#         elif output_format == "pdf":
#             return create_pdf_resume(resume_data)
#         else:
#             raise ValueError("Unsupported output format. Choose 'latex' or 'pdf'.")

from io import BytesIO
from jinja2 import Environment, FileSystemLoader
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

env = Environment(
    loader=FileSystemLoader('.'),
    block_start_string='((%',
    block_end_string='%))',
    variable_start_string='(((',
    variable_end_string=')))',
    comment_start_string='((#',
    comment_end_string='#))',
)

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


# ---------------- LaTeX Resume Builder ---------------- #
def create_latex_resume(data: dict) -> str:
    def escape_latex(text):
        if not text:
            return ""
        # Use single backslash for proper LaTeX escaping
        return (
            str(text)
            .replace("&", r"\&")
            .replace("%", r"\%")
            .replace("$", r"\$")
            .replace("#", r"\#")
            .replace("_", r"\_")
            .replace("{", r"\{")
            .replace("}", r"\}")
            .replace("~", r"\textasciitilde{}")
            .replace("^", r"\textasciicircum{}")
        )

    name = escape_latex(data.get("name", ""))
    email = escape_latex(data.get("email", ""))
    phone = escape_latex(data.get("phone", ""))
    github_url = escape_latex(data.get("github", ""))
    linkedin_url = escape_latex(data.get("linkedin", ""))
    summary = escape_latex(data.get("summary", ""))
    skills = escape_latex(data.get("skills", ""))

    experience_latex = ""
    for exp in data.get("experience", []):
        title = escape_latex(exp.get("title", ""))
        company = escape_latex(exp.get("company", ""))
        years = escape_latex(exp.get("years", ""))
        # Accept either string or list for description
        desc_raw = exp.get("description", "")
        if isinstance(desc_raw, list):
            desc_raw = "\n".join(desc_raw)
        description = escape_latex(desc_raw).replace("\n", r"\\")
        experience_latex += f"\\textbf{{{title}}} at \\textit{{{company}}} ({years})\\\\\n"
        if description:
            experience_latex += description + r"\\\vspace{0.1cm}" + "\n"

    education_latex = ""
    for edu in data.get("education", []):
        degree = escape_latex(edu.get("degree", ""))
        university = escape_latex(edu.get("university", ""))
        graduation_year = escape_latex(edu.get("graduation_year", ""))
        desc_raw = edu.get("description", "")
        if isinstance(desc_raw, list):
            desc_raw = "\n".join(desc_raw)
        description = escape_latex(desc_raw).replace("\n", r"\\")
        education_latex += f"\\textbf{{{degree}}}, \\textit{{{university}}} ({graduation_year})\\\\\n"
        if description:
            education_latex += description + r"\\\vspace{0.1cm}" + "\n"

    projects_latex = ""
    for proj in data.get("projects", []):
        proj_name = escape_latex(proj.get("name", ""))
        technologies = escape_latex(proj.get("technologies", ""))
        desc_raw = proj.get("description", "")
        if isinstance(desc_raw, list):
            desc_raw = "\n".join(desc_raw)
        description = escape_latex(desc_raw).replace("\n", r"\\")
        link = escape_latex(proj.get("link", ""))
        projects_latex += f"\\textbf{{{proj_name}}}\\\\\n"
        if technologies:
            projects_latex += f"\\textit{{Technologies:}} {technologies}\\\\\n"
        if description:
            projects_latex += description + r"\\\n"
        if link:
            projects_latex += f"Link: \\url{{{link}}}\\\\\n"
        projects_latex += r"\vspace{0.1cm}" + "\n"

    certifications_latex = ""
    for cert in data.get("certifications", []):
        cert_name = escape_latex(cert.get("name", ""))
        organization = escape_latex(cert.get("organization", ""))
        date_issued = escape_latex(cert.get("date_issued", ""))
        certifications_latex += (
            f"\\textbf{{{cert_name}}} from {organization} ({date_issued})\\\\\n"
        )
        certifications_latex += r"\vspace{0.1cm}" + "\n"

    languages_latex = ""
    for lang in data.get("languages", []):
        language = escape_latex(lang.get("language", ""))
        proficiency = escape_latex(lang.get("proficiency", ""))
        languages_latex += f"{language} (\\textit{{{proficiency}}})\\\\\n"
        languages_latex += r"\vspace{0.1cm}" + "\n"

    awards_latex = ""
    for award in data.get("awards", []):
        award_name = escape_latex(award.get("name", ""))
        organization = escape_latex(award.get("organization", ""))
        date = escape_latex(award.get("date", ""))
        awards_latex += f"\\textbf{{{{{award_name}}}}} from {organization} ({date})\\\\\n"
        awards_latex += r"\vspace{0.1cm}" + "\n"

    latex_content = fr"""
\documentclass[10pt, a4paper]{{article}}
\usepackage[utf8]{{inputenc}}
\usepackage[T1]{{fontenc}}
\usepackage{{geometry}}
\geometry{{left=1in, right=1in, top=1in, bottom=1in}}
\usepackage{{enumitem}}
\setlist[itemize]{{noitemsep, topsep=0pt, parsep=0pt, partopsep=0pt}}
\usepackage{{hyperref}}
\hypersetup{{
    colorlinks=true,
    urlcolor=blue,
}}
\usepackage{{helvet}} % Use Helvetica font
\renewcommand{{\familydefault}}{{\sfdefault}} % Set sans-serif as default font

\begin{{document}}

\begin{{center}}
    {{\fontsize{{28pt}}{{32pt}}\selectfont \textbf{{{name}}}}}\\
    \\[5pt] % Add some vertical space
    {{\fontsize{{11pt}}{{14pt}}\selectfont {email} $|$ {phone}}}\\
    \\[2pt] % Add some vertical space
    {{\fontsize{{11pt}}{{14pt}}\selectfont \href{{{github_url}}}{{GitHub}} $|$ \href{{{linkedin_url}}}{{LinkedIn}}}}
\end{{center}}

\section*{{\fontsize{{16pt}}{{20pt}}\selectfont Summary}}
{summary}

\section*{{\fontsize{{16pt}}{{20pt}}\selectfont Experience}}
{experience_latex}

\section*{{\fontsize{{16pt}}{{20pt}}\selectfont Education}}
{education_latex}

\section*{{\fontsize{{16pt}}{{20pt}}\selectfont Projects}}
{projects_latex}

\section*{{\fontsize{{16pt}}{{20pt}}\selectfont Skills}}
{skills}

\section*{{\fontsize{{16pt}}{{20pt}}\selectfont Certifications}}
{certifications_latex}

\section*{{\fontsize{{16pt}}{{20pt}}\selectfont Languages}}
{languages_latex}

\section*{{\fontsize{{16pt}}{{20pt}}\selectfont Awards \& Honors}}
{awards_latex}

\end{{document}}
"""
    return latex_content

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

    def generate_resume(self, resume_data: dict, output_format: str = "latex") -> str | BytesIO:
        if output_format == "latex":
            return create_latex_resume(resume_data)
        elif output_format == "pdf":
            return create_pdf_resume(resume_data)
        else:
            raise ValueError("Unsupported output format. Choose 'latex' or 'pdf'.")