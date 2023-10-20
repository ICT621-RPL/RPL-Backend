from app import db
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from datetime import datetime
import os

extend_existing_config = os.environ.get('SQLALCHEMY_EXTEND_EXISTING', 'False') == 'True'

class Experience(db.Model):
    __tablename__ = 'tbl_experience'
    __table_args__ = {'extend_existing': extend_existing_config}  # Ensure table isn't recreated

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
    __table_args__ = {'extend_existing': extend_existing_config}  # Ensure table isn't recreated

    document_id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, ForeignKey('tbl_rpl_application.application_id'), nullable=False)
    file_name = db.Column(db.String(100))
    file_path = db.Column(db.String(250))

    def __init__(self, application_id, file_name, file_path):
        self.application_id = application_id
        self.file_name = file_name
        self.file_path = file_path

class Recommendation(db.Model):
    __tablename__ = 'tbl_recommendation'
    __table_args__ = {'extend_existing': extend_existing_config}  # Ensure table isn't recreated

    recommendation_id = db.Column(db.Integer, primary_key=True)
    experience_id = db.Column(db.Integer, ForeignKey('tbl_experience.experience_id'), nullable=False)
    recommendation_unit_code = db.Column(db.String(20))
    recommendation_unit_name = db.Column(db.String(250))
    recommendation_similarity = db.Column(db.Float)
    is_applied = db.Column(db.Integer, default=0)
    status_id = db.Column(db.Integer, ForeignKey('tbl_status_master.status_id'), nullable=False)

    def __init__(self, experience_id, recommendation_unit_code, unit_name, similarity, is_applied, status_id):
       self.experience_id = experience_id
       self.recommendation_unit_code = recommendation_unit_code
       self.is_applied = is_applied
       self.status_id = status_id
       self.recommendation_unit_name = unit_name
       self.recommendation_similarity = similarity

    def to_dict(self):
        return {
            'recommendation_id': self.recommendation_id,
            'experience_id': self.experience_id,
            'recommendation_unit_code': self.recommendation_unit_code,
            'is_applied': self.is_applied
        }

class RplApplication(db.Model):
    __tablename__ = 'tbl_rpl_application'
    __table_args__ = {'extend_existing': extend_existing_config}  # Ensure table isn't recreated

    application_id = db.Column(db.Integer, primary_key=True)
    application_date = db.Column(db.DateTime, default=datetime.utcnow)
    student_id = db.Column(db.Integer)

     # Adding a relationships
    documents = relationship('ExperienceDocument', backref='experience', cascade="all, delete-orphan")

    def __init__(self, application_date, student_id):
       if application_date is None:
           application_date = datetime.utcnow()
       self.application_date = application_date
       self.student_id = student_id

class Status(db.Model):
    __tablename__ = 'tbl_status_master'
    __table_args__ = {'extend_existing': extend_existing_config}  # Ensure table isn't recreated

    status_id = db.Column(db.Integer, primary_key=True)
    status_name = db.Column(db.String(250))

    # Adding a relationships
    recommendation = relationship('Recommendation', backref='recommendation')

    def __init__(self, status_id, status_name):
       self.status_id = status_id
       self.status_name = status_name