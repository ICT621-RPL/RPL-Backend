import re, os, smtplib
from flask_mail import Mail
from email.message import EmailMessage

mail = Mail()

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

    # experience_html = generate_experience_html(experience_details, recommendations)
    # msg.add_alternative(experience_html, subtype="html")

    # for document in experience_document_paths:
    #     document_path = (
    #         document.file_path
    #     )  # Change this if it's another name or a method
    #     absolute_path = os.path.abspath(document_path)

    #     # Determine MIME type and read the file
    #     if absolute_path.endswith(".pdf"):
    #         mime_type = "application/pdf"
    #     elif absolute_path.endswith(".docx"):
    #         mime_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    #     elif absolute_path.endswith(".doc"):
    #         mime_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    #     else:
    #         print(f"Unsupported file type for {absolute_path}. Skipping.")
    #         continue

    #     try:
    #         with open(absolute_path, "rb") as fp:
    #             file_name = os.path.basename(absolute_path)
    #             file_content = fp.read()
    #             msg.add_attachment(
    #                 file_content,
    #                 maintype=mime_type.split("/")[0],
    #                 subtype=mime_type.split("/")[1],
    #                 filename=file_name,
    #             )
    #     except Exception as e:
    #         print(f"Error reading {absolute_path}: {e}")

    # Using SMTP_SSL for secure connection
    with smtplib.SMTP_SSL(mail_server, mail_port) as server:
        server.login(mail_username, mail_password)
        server.send_message(msg)


# Helper function to generate HTML from experience details
def generate_experience_html(experience_details, recommendations):
    content = os.environ.get("MAIL_INTRO") + "<br/>"
    for experience in experience_details:
        content += """
        <h2>{}</h2>
        <ul>
            <li>
                <p>{} {} - {} {}</p>
                <p>{}</p>
                <p>{}</p>
                <p>{}</p>
            </li>
        </ul>
        """.format(
            experience.job_title,
            experience.from_month,
            experience.from_year,
            experience.to_month,
            experience.to_year,
            experience.company,
            experience.country,
            experience.description,
        )

    content += os.environ.get("MAIL_RECOMMENDATION_INTRO") + "<br/>"
    for recommendation in recommendations:
        content += """
        <ul>
            <li>
                <p>{}</p>
            </li>
        </ul>
        """.format(
            recommendation['recommendation_unit_code']
        )

    return content
