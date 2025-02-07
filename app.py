from flask import Flask, render_template, request, redirect, url_for, send_file, current_app
from models import db, Resume
from forms import ResumeForm
from resume_generator import generate_pdf
import requests
import os
import json

# Initialize Flask application
app = Flask(__name__)
app.config.from_pyfile("config.py")
db.init_app(app)

# Constants
TEMPLATE_FOLDER = "templates"
RESUME_PDF_FOLDER = "resume_pdfs"

# Ensure necessary directories exist
os.makedirs(TEMPLATE_FOLDER, exist_ok=True)
os.makedirs(RESUME_PDF_FOLDER, exist_ok=True)

def get_geolocation():
    """
    Fetch the user's geolocation using the IPStack API.
    """
    try:
        api_key = current_app.config["IPSTACK_API_KEY"]
        user_ip = request.remote_addr

        # Fallback IP for localhost development
        if user_ip == "127.0.0.1":
            user_ip = "8.8.8.8"

        # Build the API URL
        url = f"http://api.ipstack.com/{user_ip}?access_key={api_key}"
        response = requests.get(url)
        data = response.json()

        # Extract relevant geolocation details
        location = {
            "city": data.get("city", "Unknown City"),
            "region": data.get("region_name", "Unknown Region"),
            "country": data.get("country_name", "Unknown Country"),
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude"),
        }
        return location
    except Exception as e:
        return {"error": str(e)}

@app.route("/", methods=["GET", "POST"])
def index():
    """
    Render the home page with the resume form and handle form submissions.
    """
    form = ResumeForm()

    # Fetch geolocation data to auto-fill the address field
    geolocation = get_geolocation()
    if "error" not in geolocation and request.method == "GET":
        form.address.data = f"{geolocation.get('city')}, {geolocation.get('region')}, {geolocation.get('country')}"

    if form.validate_on_submit():
        # Extract structured experience data
        experience_data = [
            {"date": exp_form.date.data, "position": exp_form.position.data, "details": exp_form.details.data}
            for exp_form in form.experience
        ] if form.experience else []

        # Create a new Resume object
        new_resume = Resume(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            address=form.address.data,
            objective=form.objective.data or "N/A",
            education=form.education.data or "N/A",
            experience=json.dumps(experience_data),  # Store experience as JSON
            skills=form.skills.data or "N/A",
            projects=form.projects.data or "N/A",
            references=form.references.data or "N/A",
            template=int(form.template.data),
        )
        db.session.add(new_resume)
        db.session.commit()

        # Generate the PDF for the resume
        resume_path = generate_pdf(new_resume)
        if not resume_path:
            return "Error: Failed to generate PDF.", 500

        return redirect(url_for("view_resume", resume_id=new_resume.id))

    return render_template("index.html", form=form)

@app.route("/resume/<int:resume_id>")
def view_resume(resume_id):
    """
    View the generated resume using the selected template.
    """
    resume = Resume.query.get_or_404(resume_id)

    # Ensure all fields exist
    resume_data = {
        "name": resume.name,
        "email": resume.email,
        "phone": resume.phone,
        "address": resume.address,
        "objective": resume.objective or "Not Provided",
        "education": resume.education or "Not Provided",
        "experience": json.loads(resume.experience) if resume.experience else [],
        "skills": resume.skills or "Not Provided",
        "projects": resume.projects or "Not Provided",
        "references": resume.references or "Not Provided",
    }

    template_file = f"template{resume.template}.html"

    # Check if the template exists
    if not os.path.exists(os.path.join(TEMPLATE_FOLDER, template_file)):
        return f"Error: Template {template_file} not found.", 404

    return render_template(template_file, resume=resume_data)

@app.route("/download/<int:resume_id>")
def download_resume(resume_id):
    """
    Download the generated resume PDF.
    """
    resume = Resume.query.get_or_404(resume_id)
    resume_path = os.path.join(RESUME_PDF_FOLDER, f"resume_{resume.id}.pdf")

    # Verify the PDF exists before sending it
    if not os.path.exists(resume_path):
        return f"Error: Resume PDF not found for ID {resume_id}.", 404

    return send_file(resume_path, as_attachment=True)

@app.errorhandler(404)
def not_found_error(error):
    """
    Handle 404 errors with a custom message.
    """
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_error(error):
    """
    Handle 500 errors with a custom message.
    """
    db.session.rollback()
    return render_template("500.html"), 500

if __name__ == "__main__":
    app.run(debug=True)
