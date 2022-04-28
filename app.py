from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
engine = create_engine('sqlite:///db.sqlite')


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


@app.route('/')
def home():
    """
        Lists all todo items
    """
    todo_list = Todo.query.all()
    print(type(todo_list))
    return render_template("index.html", todo_list=todo_list)


@app.route("/add", methods=["POST"])
def add():
    """
        Creates new todo items
    """
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/update/<int:todo_id>")
def update(todo_id):
    """
        Updates todo items
    """
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    """
        Deletes todo items
    """
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))


query = """
        SELECT *
        FROM todo
        WHERE id > 5
    """


@app.route("/raw_sql")
def raw_sql():
    """
        Retrives all todos where the id > 5
    :return: list
    """
    with engine.connect() as con:
        rs = con.execute(query).fetchall()
    return render_template("index.html", todo_list=rs)


db.create_all()
