from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    task_type = db.Column(db.String(50))
    description = db.Column(db.Text)
    priority = db.Column(db.String(10))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

with app.app_context():
    db.create_all()

@app.route("/")
def homePage():
    return render_template("homepage.html", pagetitle="Home Page")

@app.route('/add', methods=['POST'])
def add():
    content = request.form['content']
    task_type = request.form.get('task_type')
    description = request.form.get('description')
    priority = request.form.get('priority')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')

    try:
        new_task = Todo(
            content=content,
            task_type=task_type,
            description=description,
            priority=priority,
            start_date=datetime.strptime(start_date, '%Y-%m-%d').date() if start_date else None,
            end_date=datetime.strptime(end_date, '%Y-%m-%d').date() if end_date else None
        )
        db.session.add(new_task)
        db.session.commit()
        return render_template('confirm.html', pagetitle="Confirmation Page", task=content)
    except Exception as e:
        return f"Failed to add task: {str(e)}", 500

@app.route('/update', methods=['GET', 'POST'])
def update():
    tasks = Todo.query.order_by(Todo.date_created.desc()).limit(5).all()
    if request.method == 'POST':
        task_id = int(request.form['task_id'])
        task = Todo.query.get(task_id)

        if task:
            try:
                task.content = request.form['content']
                task.task_type = request.form.get('task_type')
                task.description = request.form.get('description')
                task.priority = request.form.get('priority')

                start_date = request.form.get('start_date')
                end_date = request.form.get('end_date')

                task.start_date = datetime.strptime(start_date, '%Y-%m-%d').date() if start_date else None
                task.end_date = datetime.strptime(end_date, '%Y-%m-%d').date() if end_date else None

                db.session.commit()
                return render_template('update_result.html', success=True)
            except Exception as e:
                return render_template('update_result.html', success=False, error_message=str(e))
        else:
            return render_template('update_result.html', success=False, error_message="Task not found.")
    return render_template('update.html', pagetitle="Update Page", tasks=tasks)

#  Run on port 8000
if __name__ == "__main__":
    app.run(debug=True, port=8000)
