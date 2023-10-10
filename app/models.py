from app import db
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from datetime import datetime

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

    # Adding a relationships
    documents = relationship('ExperienceDocument', backref='experience', cascade="all, delete-orphan")
    recommendations = relationship('Recommendation', backref='experience', cascade="all, delete-orphan")

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

    def to_dict(self):
        return {
            'experience_id': self.experience_id,
            'studentId': self.student_id,
            'jobTitle': self.job_title,
            'fromMonth': self.from_month,
            'fromYear': self.from_year,
            'toMonth': self.to_month,
            'toYear': self.to_year,
            'company': self.company,
            'country': self.country,
            'description': self.description
        }

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

class Recommendation(db.Model):
    __tablename__ = 'tbl_recommendation'
    __table_args__ = {'extend_existing': True}  # Ensure table isn't recreated

    recommendation_id = db.Column(db.Integer, primary_key=True)
    experience_id = db.Column(db.Integer, ForeignKey('tbl_experience.experience_id'), nullable=False)
    recommendation_unit_code = db.Column(db.String(20))
    is_applied = db.Column(db.Integer, default=0)

    def __init__(self, experience_id, recommendation_unit_code, is_applied):
       self.experience_id = experience_id
       self.recommendation_unit_code = recommendation_unit_code
       self.is_applied = is_applied

    def to_dict(self):
        return {
            'recommendation_id': self.recommendation_id,
            'experience_id': self.experience_id,
            'recommendation_unit_code': self.recommendation_unit_code,
            'is_applied': self.is_applied
        }

class RplApplication(db.Model):
    __tablename__ = 'tbl_rpl_application'
    __table_args__ = {'extend_existing': True}  # Ensure table isn't recreated

    application_id = db.Column(db.Integer, primary_key=True)
    application_date = db.Column(db.DateTime, default=datetime.utcnow)
    student_id = db.Column(db.Integer)
    # experience_id = db.Column(db.Integer, ForeignKey('tbl_experience.experience_id'), nullable=False)

    def __init__(self, application_date, student_id):
       if application_date is None:
           application_date = datetime.utcnow()
       self.application_date = application_date
       self.student_id = student_id
    #    self.experience_id = experience_id