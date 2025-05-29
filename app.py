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
    task_content = request.form['content']
    task_type = request.form.get('task_type')
    description = request.form.get('description')
    priority = request.form.get('priority')
    start_date = datetime.strptime(request.form['start_date'], "%Y-%m-%d").date()
    end_date = datetime.strptime(request.form['end_date'], "%Y-%m-%d").date()
    new_task = Todo(
        content=task_content,
        task_type=task_type,
        description=description,
        priority=priority,
        start_date=start_date,
        end_date=end_date
    )

    try:
        db.session.add(new_task)
        db.session.commit()
        return render_template('confirm.html', pagetitle="Confirmation Page", task=new_task)
    except Exception as e:
        return f"Failed to add task: {e}"



@app.route('/update', methods=['GET', 'POST'])
def update():
    tasks = Todo.query.order_by(Todo.date_created.desc()).limit(5).all()
    
    if request.method == 'POST':
        task_id = int(request.form['task_id'])
        new_content = request.form['content']
        new_description = request.form.get('description', '')
        start_date_str = request.form.get('start_date', '')
        end_date_str = request.form.get('end_date', '')

        task = Todo.query.get(task_id)

        if task:
            task.content = new_content
            task.description = new_description

            if start_date_str:
                task.start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            if end_date_str:
                task.end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

            try:
                db.session.commit()
                return render_template('confirm.html', pagetitle="Confirmation Page", task=task)
            except Exception as e:
                return f"Failed to update task: {e}"

        else:
            return "Task not found!", 404

    return render_template('update.html', pagetitle="Update Page", tasks=tasks)

#  Run on port 8000
if __name__ == "__main__":
    app.run(debug=True, port=8000)
