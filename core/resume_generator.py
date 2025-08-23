from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter


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
        leading=13,  # slightly tighter like your resume
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

    # Name
    story.append(Paragraph(data.get("name", ""), styles["ResumeName"]))

    # Contact Info with GitHub/LinkedIn hyperlinks
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

    # Education
    if data.get("education"):
        add_section("EDUCATION")
        for edu in data["education"]:
            story.append(Paragraph(
                f"<b>{edu.get('degree','')}</b>, {edu.get('university','')} ({edu.get('graduation_year','')})",
                styles["ContentText"]
            ))
            if edu.get("description"):
                for line in edu["description"].split("\n"):
                    if line.strip():
                        story.append(Paragraph(line, styles["BulletText"]))

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

    # Awards
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
