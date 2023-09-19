from app import db

class Experience(db.Model):
    __tablename__ = 'tbl_experience'
    __table_args__ = {'extend_existing': True}  # Ensure table isn't recreated

    experience_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer)
    job_title = db.Column(db.String(250))
    from_date = db.Column(db.DateTime)
    to_date = db.Column(db.DateTime)
    experience = db.Column(db.Text)

    def __init__(self, studentId, jobTitle, fromDate, toDate, experience):
        self.student_id = studentId
        self.job_title = jobTitle
        self.from_date = fromDate
        self.to_date = toDate
        self.experience = experience
