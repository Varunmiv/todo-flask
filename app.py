from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Task {self.id}>'

# Create the database
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    tasks = Task.query.all()  # Fetch all tasks from DB
    return render_template('index.html', todos=tasks)

@app.route('/add', methods=['POST'])
def add():
    task_content = request.form.get('task')
    if task_content:
        new_task = Task(content=task_content)
        db.session.add(new_task)
        db.session.commit()
    return redirect('/')

@app.route('/delete/<int:task_id>')
def delete(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect('/')

@app.route('/update/<int:task_id>', methods=['POST'])
def update(task_id):
    task = Task.query.get(task_id)
    if task:
        task.content = request.form.get('content')
        db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
