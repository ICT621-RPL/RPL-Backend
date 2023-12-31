import re, os, smtplib
from flask_mail import Mail
from email.message import EmailMessage, Message
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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

# Helper function for data preprocessing and feature extraction
def process_text(text):
    if isinstance(text, str):
        text = re.sub(r'UNLO\d+\|\d+\|', '', text)  # Remove 'UNLO' patterns
        text = text.lower()  # Convert to lowercase
        text = re.sub('<[^>]+>', '', text)  # Remove HTML tags
        text = re.sub(r'[^\w\s]', '', text)  # Remove special characters and symbols
        stop_words = set(stopwords.words('english'))  # Set of English stopwords
        word_tokens = word_tokenize(text)  # Tokenize the text into words
        filtered_text = [word for word in word_tokens if word not in stop_words]  # Remove stopwords
        # Perform stemming or lemmatization if required
        # Join the remaining words back into a string
        text = ' '.join(filtered_text)
        return text
    else:
        return ''


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
def recommendation_to_dict(recommendations):
    recommendations_array = []
    for unit_code, unit_name, similarity in recommendations:
        recommendations_dict = {
            "recommendation_unit_code": unit_code,
            "recommendation_unit_name": unit_name,
            "recommendation_similarity": similarity
        }
        recommendations_array.append(recommendations_dict)

    return recommendations_array


# Helper function to send email
def send_email_to_advance_standing_team(application_id):
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

def send_email_to_applicant(email_content, recipient):
    recipient_email = check_student_id(recipient)
    mail_server = os.environ.get("MAIL_SERVER")
    mail_port = os.environ.get("MAIL_PORT")
    mail_username = os.environ.get("MAIL_USERNAME")
    mail_password = os.environ.get("MAIL_PASSWORD")

    msg = MIMEMultipart()
    msg.attach(MIMEText(email_content, 'html'))
    msg["Subject"] = "Application Status"
    msg["From"] = mail_username
    msg["To"] = recipient_email

    # Using SMTP_SSL for secure connection
    with smtplib.SMTP_SSL(mail_server, mail_port) as server:
        server.login(mail_username, mail_password)
        server.send_message(msg)

def check_student_id(student_id):
    # Regular expression for validating an Email
    regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    
    if re.match(regex, student_id):
        return student_id
    elif student_id.isdigit():
        return student_id+"@student.murdoch.edu.au"
    else:
        return "Invalid"
