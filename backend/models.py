from config import db

class Student(db.Model):
    dir_id = db.Column(db.String(80), primary_key=True)
    first_name = db.Column(db.String(80), unique=False, nullable=True)
    last_name = db.Column(db.String(80), unique=False, nullable=True)
    insta_handle = db.Column(db.String(80), unique=True, nullable=True)
    course1 = db.Column(db.String(80), nullable=True)
    course2 = db.Column(db.String(80), nullable=True)
    course3 = db.Column(db.String(80), nullable=True)
    course4 = db.Column(db.String(80), nullable=True)
    course5 = db.Column(db.String(80), nullable=True)
    course6 = db.Column(db.String(80), nullable=True)
    course7 = db.Column(db.String(80), nullable=True)
    course8 = db.Column(db.String(80), nullable=True)

    def to_json(self):
        return {
            "dir_id": self.dir_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "insta_handle": self.insta_handle,
            "course1": self.course1,
            "course2": self.course2,
            "course3": self.course3,
            "course4": self.course4,
            "course5": self.course5,
            "course6": self.course6,
            "course7": self.course7,
            "course8": self.course8, 
        }
        