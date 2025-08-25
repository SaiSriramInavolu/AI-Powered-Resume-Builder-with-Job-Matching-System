from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.platypus import Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
import google.generativeai as genai
import os

def generate_ai_summary(data: dict, user_summary: str = "") -> str:
    """
    Generate a professional summary using Gemini 2.5 Flash.
    If user_summary is provided, refine it using AI with other form data.
    Otherwise, generate a fresh summary.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return "Experienced professional with a passion for technology and innovation."  

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")

    education = "; ".join(
        [f"{e.get('degree','')} in {e.get('stream','')} from {e.get('university','')} ({e.get('graduation_year','')})"
         for e in data.get("education", []) if e]
    )
    experience = "; ".join(
        [f"{x.get('title','')} at {x.get('company','')} ({x.get('years','')})"
         for x in data.get("experience", []) if x]
    )
    projects = "; ".join(
        [f"{p.get('name','')} ({p.get('technologies','')})"
         for p in data.get("projects", []) if p]
    )
    skills = data.get("skills", "")

    if user_summary:
        prompt = f"""The user has written this summary:
{user_summary}

Please refine and improve it into a professional resume summary. 
Incorporate key details from their education, experience, projects, and skills:

Education: {education}
Experience: {experience}
Projects: {projects}
Skills: {skills}

Return only the polished professional summary text."""
    else:
        prompt = f"""Generate a professional resume summary from the following details:

Education: {education}
Experience: {experience}
Projects: {projects}
Skills: {skills}

Return only the professional summary text."""

    response = model.generate_content(prompt)
    return response.text.strip() if response and response.text else ""
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

    # Custom Styles
    styles.add(ParagraphStyle(
        name="ResumeName",
        fontSize=20,
        leading=24,
        fontName="Helvetica-Bold",
        alignment=TA_CENTER,
    ))
    styles.add(ParagraphStyle(
        name="SectionHeading",
        fontSize=13,
        leading=16,
        fontName="Helvetica-Bold",
        alignment=TA_LEFT,
        spaceBefore=12,
        spaceAfter=4,
        textTransform="uppercase",
    ))
    styles.add(ParagraphStyle(
        name="ContentText",
        fontSize=11,
        leading=14,
        fontName="Helvetica",
        alignment=TA_LEFT,
    ))
    styles.add(ParagraphStyle(
        name="BulletText",
        fontSize=11,
        leading=13,  
        fontName="Helvetica",
        alignment=TA_LEFT,
        leftIndent=15,
        bulletIndent=5,
    ))
    styles.add(ParagraphStyle(
        name="ContactInfo",
        fontSize=10,
        leading=12,
        fontName="Helvetica",
        alignment=TA_CENTER,
    ))

    story = []

   
    story.append(Paragraph(data.get("name", ""), styles["ResumeName"]))

    contact_items = []
    if data.get("phone"):
        contact_items.append(data["phone"])
    if data.get("email"):
        contact_items.append(data["email"])
    if data.get("github"):
        contact_items.append(f'<a href="{data["github"]}">GitHub</a>')
    if data.get("linkedin"):
        contact_items.append(f'<a href="{data["linkedin"]}">LinkedIn</a>')

    if contact_items:
        story.append(Paragraph(" | ".join(contact_items), styles["ContactInfo"]))

    story.append(Spacer(1, 0.15 * inch))

    def add_section(title):
        """Helper to add section heading with line."""
        story.append(Paragraph(title, styles["SectionHeading"]))
        story.append(HRFlowable(width="100%", thickness=0.8, color="black", spaceBefore=2, spaceAfter=6))
        story.append(Spacer(1, 0.04 * inch))

    # Summary
    if data.get("summary"):
        add_section("SUMMARY")
        story.append(Paragraph(data["summary"], styles["ContentText"]))

    from reportlab.pdfbase.pdfmetrics import stringWidth

    # Education
    if data.get("education"):
        add_section("EDUCATION")
        max_width = 400  

        for edu in data["education"]:
            degree_line = f"<b>{edu.get('degree','')}</b>"
            if edu.get("stream"):
                degree_line += f" in <b>{edu['stream']}</b>"
            if edu.get("university"):
                degree_line += f", {edu['university']}"
            if edu.get("graduation_year"):
                degree_line += f" ({edu['graduation_year']})"

            if edu.get("cgpa"):
                cgpa_text = f"<b>CGPA/Percentage:</b> {edu['cgpa']}"
                line_width = stringWidth(degree_line, "Helvetica", 11)

                if line_width < max_width:
                    # Left = degree/university, Right = CGPA
                    table = Table(
                        [[Paragraph(degree_line, styles["ContentText"]),
                        Paragraph(cgpa_text, styles["ContentText"])]],
                        colWidths=[None, 130]
                    )
                    table.setStyle(TableStyle([
                        ("ALIGN", (0, 0), (0, 0), "LEFT"),
                        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("LEFTPADDING", (0, 0), (-1, -1), 0),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                        ("TOPPADDING", (0, 0), (-1, -1), 0),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                    ]))
                    story.append(table)
                else:
                    # Too long → CGPA on next line, no indent
                    story.append(Paragraph(degree_line, styles["ContentText"]))
                    story.append(Paragraph(cgpa_text, styles["ContentText"]))
            else:
                story.append(Paragraph(degree_line, styles["ContentText"]))

            # # Description (bullets)
            # if edu.get("description"):
            #     for line in edu["description"].split("\n"):
            #         if line.strip():
            #             story.append(Paragraph(line, styles["BulletText"]))




    # Experience
    if data.get("experience"):
        add_section("EXPERIENCE")
        for exp in data["experience"]:
            story.append(Paragraph(
                f"<b>{exp.get('title','')}</b> | {exp.get('company','')} ({exp.get('years','')})",
                styles["ContentText"]
            ))
            if exp.get("description"):
                for line in exp["description"].split("\n"):
                    if line.strip():
                        story.append(Paragraph(line, styles["BulletText"]))

    # Projects
    if data.get("projects"):
        add_section("PROJECTS")
        for proj in data["projects"]:
            story.append(Paragraph(f"<b>{proj.get('name','')}</b>", styles["ContentText"]))
            if proj.get("description"):
                for line in proj["description"].split("\n"):
                    if line.strip():
                        story.append(Paragraph(line, styles["BulletText"]))
            if proj.get("technologies"):
                story.append(Paragraph(f"<i>Technologies:</i> {proj['technologies']}", styles["BulletText"]))
            if proj.get("link"):
                story.append(Paragraph(f'<i>Project Link:</i> <a href="{proj["link"]}">{proj["link"]}</a>', styles["BulletText"]))

    # Skills
    if data.get("skills"):
        add_section("TECHNICAL SKILLS")
        if isinstance(data["skills"], dict):
            for cat, skills in data["skills"].items():
                story.append(Paragraph(f"<b>{cat}:</b> {', '.join(skills)}", styles["ContentText"]))
        else:
            story.append(Paragraph(data["skills"], styles["ContentText"]))

    # Certifications
    if data.get("certifications"):
        add_section("CERTIFICATIONS")
        for cert in data["certifications"]:
            story.append(Paragraph(
                f"<b>{cert.get('name','')}</b> – {cert.get('organization','')} ({cert.get('date_issued','')})",
                styles["ContentText"]
            ))

    # Languages
    if data.get("languages"):
        add_section("LANGUAGES")
        for lang in data["languages"]:
            story.append(Paragraph(
                f"{lang.get('language','')} ({lang.get('proficiency','')})",
                styles["ContentText"]
            ))

    
    if data.get("awards"):
        add_section("AWARDS & HONORS")
        for award in data["awards"]:
            story.append(Paragraph(
                f"<b>{award.get('name','')}</b> – {award.get('organization','')} ({award.get('date','')})",
                styles["ContentText"]
            ))

    doc.build(story)
    buffer.seek(0)
    return buffer
