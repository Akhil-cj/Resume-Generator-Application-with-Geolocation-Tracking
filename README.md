Resume Generator Application

Overview

This project is a Resume Generator Application with Geolocation Tracking. Users can create resumes using different templates, autofill location details using the IPStack API, and download resumes as PDFs.

Features

Form-based resume creation

Auto-filled location using IPStack API

Multiple resume templates

PDF generation

Database integration (MySQL/MongoDB)

Installation & Setup

1. Clone the Repository

git clone <your-repo-url>
cd resumeeee

2. Backend Setup

Install Dependencies

cd backend
pip install -r requirements.txt

Configure Environment Variables

Create a .env file in the backend/ directory and add:

IPSTACK_API_KEY=your_api_key_here
DATABASE_URL=mysql://user:password@localhost/resume_db

Run Backend Server

python app.py

3. Frontend Setup

Install Dependencies

cd ../frontend
npm install

Run Frontend Server

npm start

Database Setup

Ensure MySQL/MongoDB is installed and running.

Create a database named resume_db (for MySQL).

Run database migrations if needed.

PDF Generation

The backend uses reportlab to generate PDFs.

Templates are stored in backend/templates/.

PDFs are saved in backend/resume_pdfs/.

IPStack API Integration

Fetches user location based on IP.

API response is processed in backend/utils.py.

Requires an active IPStack API key.
