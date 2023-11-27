from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///opslag.db"
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

class comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)#de 200 is aantal characters ,,, nullable is dat je niet niks kan invulle
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        comment_content = request.form["content"]
        new_comment = comments(content=comment_content)
        try:
            db.session.add(new_comment)
            db.session.commit()
            return redirect("/")
        except:
            return "probleeem met het oposlaan "
    else:
        commentss = comments.query.order_by(comments.date_created).all()
        return render_template("index.html", commentss=commentss)

@app.route("/delete/<int:id>")
def delete(id):
    commentsVerwijder = comments.query.get_or_404(id)
    try:
        db.session.delete(commentsVerwijder)
        db.session.commit()
        return redirect("/")
    except:
        return "werk ni haha"

if __name__ == "__main__":
    app.run(debug=True)#debug false als niet bezig bent