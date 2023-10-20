import re, os, smtplib
from flask_mail import Mail
from email.message import EmailMessage
from nltk.corpus import stopwords

mail = Mail()

ALLOWED_EXTENSIONS = {"pdf", "doc", "docx"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# Helper function to preprocess text
def preprocess_text(text):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r"[^\w\s]", "", text)  # Remove punctuation
    return text

# Helper function for data Preprocessing
def clean_text(text):
    text = re.sub(r'[^\w\s]', '', text)
    text = text.lower()
    text = ' '.join([word for word in text.split() if word not in stopwords.words('english')])
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


# Helper function to send email
def send_email(application_id, experience_details, experience_document_paths, recommendations):
    recipient_email = os.environ.get("TO_MAIL")
    mail_server = os.environ.get("MAIL_SERVER")
    mail_port = os.environ.get("MAIL_PORT")
    mail_username = os.environ.get("MAIL_USERNAME")
    mail_password = os.environ.get("MAIL_PASSWORD")

    content = (
        "Hi there,\n" +
        os.environ.get("MAIL_NOTIFICATION_MESSAGE") + "\n" +
        os.environ.get("APPLICATION_LINK") + str(application_id) + "\n"
    )

    msg = EmailMessage()
    msg.set_content(content)
    msg["Subject"] = "RPL Request for informal learning"
    msg["From"] = mail_username
    msg["To"] = recipient_email

    # Using SMTP_SSL for secure connection
    with smtplib.SMTP_SSL(mail_server, mail_port) as server:
        server.login(mail_username, mail_password)
        server.send_message(msg)
