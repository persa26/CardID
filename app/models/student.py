# from flask_sqlalchemy import SQLAlchemy
from app import db

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://test:test1234@localhost/test'
# db = SQLAlchemy(app)

class Students(db.Model):
    __tablename__ = 'Students'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    mail = db.Column(db.String(250))
    rfid = db.Column(db.String(250))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.uname,
            'surname': self.surname,
            'mail': self.mail,
            'rfid': self.rfid
        }