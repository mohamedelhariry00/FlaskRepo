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


@app.route("/")
def homePage():
    return render_template("homepage.html", pagetitle="Home Page")


if __name__ == "__main__":
    app.run(debug=True, port=9000)