import re

ALLOWED_EXTENSIONS = {"pdf", "doc", "docx"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# Function to preprocess text
def preprocess_text(text):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r"[^\w\s]", "", text)  # Remove punctuation
    return text


# Helper function to convert Experience Object to Dictionary
def experience_to_dict(exp):
    return {
        "experience_id": exp.experience_id,
        "studentId": exp.student_id,
        "jobTitle": exp.job_title,
        "fromMonth": exp.from_month,
        "fromYear": exp.from_year,
        "toMonth": exp.to_month,
        "toYear": exp.to_year,
        "company": exp.company,
        "country": exp.country,
        "description": exp.description,
    }


# Helper function to convert Experience Object to Dictionary
def recommendation_to_dict(recommendation):
    return {
        "recommendation_id": recommendation.recommendation_id,
        "experience_id": recommendation.experience_id,
        "recommendation_unit_code": recommendation.recommendation_unit_code,
        "is_applied": recommendation.is_applied,
    }
