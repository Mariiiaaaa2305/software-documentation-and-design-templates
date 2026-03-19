from flask_sqlalchemy import SQLAlchemy
import uuid

db = SQLAlchemy()

class Apartment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    price = db.Column(db.String(20))
    description = db.Column(db.Text)