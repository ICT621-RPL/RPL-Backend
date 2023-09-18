from app import db

class Experience(db.Model):
    __tablename__ = 'tbl_experience'
    __table_args__ = {'extend_existing': True}  # Ensure table isn't recreated

    experienceId = db.Column(db.Integer, primary_key=True)
    studentId = db.Column(db.Integer)
    jobTitle = db.Column(db.String(250))
    fromDate = db.Column(db.DateTime)
    toDate = db.Column(db.DateTime)
    experience = db.Column(db.Text)

    def __init__(self, studentId, jobTitle, fromDate, toDate, experience):
        self.studentId = studentId
        self.jobTitle = jobTitle
        self.fromDate = fromDate
        self.toDate = toDate
        self.experience = experience

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email
