# from flask_sqlalchemy import SQLAlchemy
from app import db

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://test:test1234@localhost/test'
# db = SQLAlchemy(app)

class GroupStudents(db.Model):
    __tablename__ = 'GroupStudents'

    id = db.Column(db.Integer, primary_key=True)
    studentId = db.Column(db.Integer)
    groupId = db.Column(db.Integer)

    def serialize(self):
        return {
            'id': self.id,
            'studentId': self.studentId,
            'groupId': self.groupId
        }