from flask import Blueprint, render_template, request, redirect, jsonify
from .models import Task, User
from . import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
main = Blueprint("main", __name__)


@main.route("/")
def index():

  page = request.args.get("page", 1, type=int)

  search = request.args.get("search", "")

  query = Task.query

  if search:
    query = query.filter(Task.title.contains(search))

  tasks = query.paginate(page=page, per_page=5)

  return render_template("index.html", tasks=tasks, search=search)

@main.route("/add", methods=["POST"])
def add():
  title = request.form["title"]

  task = Task(title=title)

  db.session.add(task)
  db.session.commit()

  return redirect("/")

@main.route("/complete/<int:id>")
def complete(id):
  task = Task.query.get_or_404(id)

  task.completed = True

  db.session.commit()

  return redirect("/")

@main.route("/delete/<int:id>")
def delete(id):

  task = Task.query.get_or_404(id)

  db.session.delete(task)
  db.session.commit()

  return redirect("/")

@main.route("/api/tasks")
@jwt_required()
def api_tasks():

  user_id = get_jwt_identity()

  tasks = Task.query.filter_by(user_id=user_id).all()

  data = []

  for task in tasks:
    data.append({
      "id": task.id,
      "title": task.title,
      "complete": task.complete
    })

  return jsonify(data)

@main.route("/api/tasks", methods=["POST"])
@jwt_required()
def api_add_task():

  user_id = get_jwt_identity()

  data = request.json

  if not data or "title" not in data:
    return jsonify({
      "status": "error",
      "message": "title is required"
    }), 400

  task = Task(
    title=data["title"],
    user_id=user_id,
    complete=False
  )

  db.session.add(task)
  db.session.commit()

  return jsonify({
    "status": "success",
    "task_id": task.id
  }), 201

@main.route("/api/task/<int:id>/complete", methods=["PUT"])
@jwt_required()
def api_complete_task(id):
  task = Task.query.get_or_404(id)
  task.complete = True
  db.session.commit()

  return jsonify({"message":"task completed"})

@main.route("/api/tasks/<int:id>", methods=["DELETE"])
@jwt_required()
def api_delete_task(id):
  user_id = get_jwt_identity()
  task = Task.query.filter_by(id=id, user_id=user_id).first_or_404()
  db.session.delete(task)
  db.session.commit()

  return jsonify({"message": "task deleted"})

@main.route("/api/register", methods=["POST"])
def register():

  data = request.json

  user = User(
    email=data["email"],
    password=generate_password_hash(data["password"])
  )

  db.session.add(user)
  db.session.commit()

  return {"message": "user created"}

@main.route("/api/login", methods=["POST"])
def login():

  data = request.json

  user = User.query.filter_by(email=data["email"]).first()

  if not user or not check_password_hash(user.password, data["password"]) :
    return {"error": "invalid credentials"}, 401
  
  token = create_access_token(identity=user.id)

  return {"token": token}