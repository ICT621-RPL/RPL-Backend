from app import db

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
