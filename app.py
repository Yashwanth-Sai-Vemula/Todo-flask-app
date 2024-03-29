from flask import Flask ,render_template,redirect,request,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    task = db.Column(db.String(200),nullable = False)
    completed = db.Column(db.Boolean,default = False)

@app.route('/')
def index():
    todos = Todo.query.all()
    return render_template('index.html',todos =todos)

@app.route('/add',methods =['POST'])
def add():
    task = request.form.get('task')
    if task:
        new_todo = Todo(task = task)
        db.session.add(new_todo)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/toggle/<int:id>')
def toggle(id):
    todo_to_toggle = Todo.query.get(id)
    if todo_to_toggle:
        todo_to_toggle.completed = not todo_to_toggle.completed
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    todo_to_delete = Todo.query.get(id)
    if todo_to_delete:
        db.session.delete(todo_to_delete)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
