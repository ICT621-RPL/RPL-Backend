from app import db
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

class Experience(db.Model):
    __tablename__ = 'tbl_experience'
    __table_args__ = {'extend_existing': True}  # Ensure table isn't recreated

    experience_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer)
    job_title = db.Column(db.String(250))
    from_month = db.Column(db.String(20))
    from_year = db.Column(db.String(20))
    to_month = db.Column(db.String(20))
    to_year = db.Column(db.String(20))
    company = db.Column(db.String(100))
    country = db.Column(db.String(20))
    description = db.Column(db.Text)

     # Adding a relationship here so that when you have an Experience instance,
    # you can easily fetch its documents
    documents = relationship('ExperienceDocument', backref='experience')

    def __init__(self, studentId, jobTitle, fromMonth, fromYear, toMonth, toYear, company, country, description):
        self.student_id = studentId
        self.job_title = jobTitle
        self.from_year = fromYear
        self.to_year = toYear
        self.from_month = fromMonth
        self.to_month = toMonth
        self.company = company
        self.country = country
        self.description = description

class ExperienceDocument(db.Model):
    __tablename__ = 'tbl_experience_document'
    __table_args__ = {'extend_existing': True}  # Ensure table isn't recreated

    document_id = db.Column(db.Integer, primary_key=True)
    experience_id = db.Column(db.Integer, ForeignKey('tbl_experience.experience_id'), nullable=False)
    file_name = db.Column(db.String(100))
    file_path = db.Column(db.String(250))

    def __init__(self, experience_id, file_name, file_path):
        self.experience_id = experience_id
        self.file_name = file_name
        self.file_path = file_path
