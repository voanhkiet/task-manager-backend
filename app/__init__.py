from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
  app = Flask(__name__)
  app.config["JWT_SECRET_KEY"] = "jwt-secret"
  app.config["SECRET_KEY"] = "secret"
  app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
  CORS(app)
  
  db.init_app(app)
  jwt.init_app(app)
  migrate.init_app(app, db)

  from .routes import main
  app.register_blueprint(main)

  with app.app_context():
    db.create_all()

  return app
  