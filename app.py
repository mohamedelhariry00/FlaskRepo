from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# Corrected database URI configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

# Optional: Disable tracking modifications to suppress warnings
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

with app.app_context():
    db.create_all()

@app.route("/")
def homePage():
    # tasks = Todo.query.all()
    return render_template("homepage.html", pagetitle="Home Page")

@app.route('/add', methods=['POST'])
def add():
    task_content = request.form['content']
    new_task = Todo(content=task_content)
    db.session.add(new_task)
    db.session.commit()
    return render_template('confirm.html', pagetitle="Confirmation Page", task=task_content)

@app.route('/update', methods=['GET', 'POST'])
def update():
    tasks = Todo.query.order_by(Todo.date_created.desc()).limit(5).all()  # Fetch last 5 tasks
    if request.method == 'POST':
        task_id = int(request.form['task_id'])  # Task ID to be updated
        new_content = request.form['content']   # Updated task content
        task = Todo.query.get(task_id)          # Fetch the task by ID
        if task:
            task.content = new_content
            db.session.commit()
            return render_template('confirm.html',pagetitle="Confirmation Page", task=new_content)
        else:
            return "Task not found!", 404
    return render_template('update.html', pagetitle="Update Page", tasks=tasks)

if __name__ == "__main__":
    app.run(debug=True, port=9000)

