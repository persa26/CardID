# from flask_sqlalchemy import SQLAlchemy
from app import db

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://test:test1234@localhost/test'
# db = SQLAlchemy(app)

class Groups(db.Model):
    __tablename__ = 'Groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.uname,
        }