import os

SECRET_KEY = "your_secret_key"  # Replace with a generated key
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost:3306/resume_db"
SQLALCHEMY_TRACK_MODIFICATIONS = False
WTF_CSRF_ENABLED = True
IPSTACK_API_KEY = "your_ipstack_api_key"
