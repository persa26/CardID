# from flask_sqlalchemy import SQLAlchemy
from app import db

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://test:test1234@localhost/test'
# db = SQLAlchemy(app)

class Employee(db.Model):
    __tablename__ = 'employee'

    id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(64))
    email = db.Column(db.String(64))
    salary = db.Column(db.Integer)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.uname,
            'email': self.email,
            'salary': self.salary
        }