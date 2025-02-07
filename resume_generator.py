from fpdf import FPDF
import os
import json

def generate_pdf(resume):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(200, 10, resume.name, ln=True, align="C")
    
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Email: {resume.email} | Phone: {resume.phone}", ln=True, align="C")
    pdf.cell(200, 10, f"Address: {resume.address}", ln=True, align="C")
    pdf.ln(10)

    sections = {
        "Objective": resume.objective,
        "Education": resume.education,
        "Work Experience": json.loads(resume.experience) if resume.experience else [],
        "Skills": resume.skills.split(", "),
        "Projects": resume.projects,
        "References": resume.references
    }

    for title, content in sections.items():
        if content:
            pdf.set_font("Arial", style="B", size=14)
            pdf.cell(0, 10, title, ln=True)
            pdf.set_font("Arial", size=12)

            if title == "Work Experience":
                for exp in content:
                    pdf.multi_cell(0, 8, f"{exp['date']} - {exp['position']}\n{exp['details']}\n", border=0)
            elif title == "Skills":
                pdf.multi_cell(0, 8, ", ".join(content))
            else:
                pdf.multi_cell(0, 8, content)
            
            pdf.ln(5)

    file_path = f"resume_pdfs/resume_{resume.id}.pdf"
    pdf.output(file_path)
    return file_path
