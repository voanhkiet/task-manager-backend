from flask import Blueprint, render_template, request, redirect, jsonify
from .models import Task
from . import db

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
def api_tasks():
  tasks = Task.query.all()

  data = []

  for task in tasks:
    data.append({
      "id": task.id,
      "title": task.title,
      "completed": task.complete
    })

  return jsonify(data)

@main.route("/api/tasks", methods=["POST"])
def api_add_task():

  data = request.json

  if not data or "title" not in data:
    return jsonify({
      "status": "error",
      "message": "title is required"
    }), 400

  task = Task(
    title=data["title"],
    complete=False
  )

  db.session.add(task)
  db.session.commit()

  return jsonify({
    "status": "success",
    "task_id": task.id
  }), 201

@main.route("/api/task/<int:id>/complete", methods=["PUT"])
def api_complete_task(id):
  task = Task.query.get_or_404(id)
  task.complete = True
  db.session.commit()

  return jsonify({"message":"task completed"})

@main.route("/api/tasks/<int:id>", methods=["DELETE"])
def api_delete_task(id):
  task = Task.query.get_or_404(id)
  db.session.delete(task)
  db.session.commit()

  return jsonify({"message": "task deleted"})