from io import BytesIO
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
            fontName="Helvetica-Bold",
            alignment=TA_CENTER,
        )
    )
    styles.add(
        ParagraphStyle(
            name="MyHeading2",
            fontSize=16,
            leading=20,
            fontName="Helvetica-Bold",
            alignment=TA_LEFT,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BodyTextSmall",
            fontSize=11,
            leading=14,
            fontName="Helvetica",
            alignment=TA_LEFT,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BodyTextBullet",
            fontSize=11,
            leading=14,
            fontName="Helvetica",
            alignment=TA_LEFT,
            leftIndent=25,
        )
    )
    styles.add(
        ParagraphStyle(
            name="ContactInfo",
            fontSize=11,
            leading=14,
            fontName="Helvetica",
            alignment=TA_CENTER,
        )
    )

    story = []

    # Name and Contact Info
    story.append(Paragraph(data.get("name", "") or "", styles["MyHeading1"]))
    story.append(Paragraph(
        f"{data.get('email', '')} | {data.get('phone', '')}"+\
        f" | <link href=\"{data['github']}\">GitHub</link>" if data.get('github') else ""+\
        f" | <link href=\"{data['linkedin']}\">LinkedIn </link>" if data.get('linkedin') else "",
        styles["ContactInfo"]
    ))
    story.append(Spacer(1, 0.3 * inch))

    # Summary
    if data.get("summary"):
        story.append(Paragraph("Summary", styles["MyHeading2"]))
        story.append(Paragraph(data["summary"], styles["BodyTextSmall"]))
        story.append(Spacer(1, 0.15 * inch))

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
            story.append(Spacer(1, 0.08 * inch))
        story.append(Spacer(1, 0.15 * inch))

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
            story.append(Spacer(1, 0.08 * inch))
        story.append(Spacer(1, 0.15 * inch))

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
            story.append(Spacer(1, 0.08 * inch))
        story.append(Spacer(1, 0.15 * inch))

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
            story.append(Spacer(1, 0.08 * inch))
        story.append(Spacer(1, 0.15 * inch))

    # Skills
    if data.get("skills"):
        story.append(Paragraph("Skills", styles["MyHeading2"]))
        story.append(Paragraph(data["skills"], styles["BodyTextSmall"]))
        story.append(Spacer(1, 0.15 * inch))

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
            story.append(Spacer(1, 0.08 * inch))
        story.append(Spacer(1, 0.15 * inch))

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
            story.append(Spacer(1, 0.08 * inch))
        story.append(Spacer(1, 0.15 * inch))

    doc.build(story)
    buffer.seek(0)
    return buffer