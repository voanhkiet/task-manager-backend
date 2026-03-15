from . import db
from datetime import datetime
class Task(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(200))
  complete = db.Column(db.Boolean, default=False)
  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)

  email = db.Column(db.String(120), unique=True)

  password = db.Column(db.String(200)) 

