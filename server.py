from flask import Flask, render_template
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


def convert_to_blob(filename):
    with open(filename, 'rb') as file:
        blob = file.read()
    return blob


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///online_shop.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    gender = db.Column(db.String(250), nullable=False)
    color = db.Column(db.String(250), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    photo1 = db.Column(db.BLOB, nullable=False)
    photo2 = db.Column(db.BLOB, nullable=False)


db.create_all()

# CREATE RECORD
new_item = Item(id=1,
                name="PUMA Carina Crew",
                gender="female",
                size=39,
                price=220,
                stock=10,
                photo1=convert_to_blob("static/img/1/b1.jpg"),
                photo2=convert_to_blob("static/img/1/b2.jpg"))

db.session.add(new_item)
db.session.commit()


@app.route('/')
def homepage():
    return render_template("index.html", current_year=datetime.now().year)


@app.route('/shop')
def shop():
    return render_template("shop.html", current_year=datetime.now().year)

@app.route('/shop/item')
def item():
    return render_template("item.html", current_year=datetime.now().year)


@app.route('/about')
def about():
    return render_template("about.html", current_year=datetime.now().year)


@app.route('/contact')
def contact():
    return render_template("contact.html", current_year=datetime.now().year)


if __name__ == "__main__":
    app.run(debug=True)
