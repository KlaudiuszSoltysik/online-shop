from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField
from wtforms.validators import EqualTo, InputRequired

from datetime import datetime

app = Flask(__name__)
app.secret_key = "password"

# CONNECT WITH DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///online_shop.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# DATABASE STRUCTURE
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(32), nullable=False)
    model = db.Column(db.String(32), nullable=False)
    gender = db.Column(db.String(8), nullable=False)
    color = db.Column(db.String(16), nullable=False)
    stock_39 = db.Column(db.Integer, nullable=True)
    stock_40 = db.Column(db.Integer, nullable=True)
    stock_41 = db.Column(db.Integer, nullable=True)
    price = db.Column(db.Integer, nullable=False)
    desc = db.Column(db.String(512), nullable=True)
    params = db.Column(db.String(512), nullable=True)
    img1 = db.Column(db.String(128), nullable=True)
    img2 = db.Column(db.String(128), nullable=True)


class LogForm(FlaskForm):
    email = StringField(label="email:", validators=[InputRequired()])
    password = PasswordField(label="password:", validators=[InputRequired()])


class RegisterForm(FlaskForm):
    email = StringField(label="email:", validators=[InputRequired()])
    password = PasswordField(label="password:", validators=[InputRequired(), EqualTo('password2', message='passwords must match')])
    password2 = PasswordField(label="repeat password:", validators=[InputRequired()])
    name = StringField(label="name and surname:", validators=[InputRequired()])
    street = StringField(label="street:", validators=[InputRequired()])
    city = StringField(label="city:", validators=[InputRequired()])


@app.route('/')
def homepage():
    return render_template("index.html", current_year=datetime.now().year)


@app.route('/shop')
def shop():
    items = db.session.query(Item).all()

    search = request.args.get("search")
    gender = request.args.get("gender")
    color = request.args.get("color")
    size = request.args.get("size")
    sort = request.args.get("sort_by")

    temp_items = []

    if gender:
        for item in items:
            if item.gender == gender:
                temp_items.append(item)

        items = temp_items.copy()
        temp_items = []

    if color:
        for item in items:
            if item.color == color:
                temp_items.append(item)

        items = temp_items.copy()
        temp_items = []

    if size == "39":
        for item in items:
            if item.stock_39:
                temp_items.append(item)

        items = temp_items.copy()
        temp_items = []

    if size == "40":
        for item in items:
            if item.stock_40:
                temp_items.append(item)

        items = temp_items.copy()
        temp_items = []

    if size == "41":
        for item in items:
            if item.stock_41:
                temp_items.append(item)

        items = temp_items.copy()
        temp_items = []

    if sort == "price":
        items.sort(key=lambda x: x.price)

    if sort == "model":
        items.sort(key=lambda x: x.model)

    return render_template("shop.html", current_year=datetime.now().year, all_items=items, gender=gender, color=color, size=size, sort=sort)


@app.route('/shop/<int:item_id>')
def item(item_id):
    item = Item.query.filter_by(id=item_id).first()
    return render_template("item.html", current_year=datetime.now().year, item=item)


@app.route('/about')
def about():
    return render_template("about.html", current_year=datetime.now().year)


@app.route('/contact')
def contact():
    return render_template("contact.html", current_year=datetime.now().year)


@app.route('/log_in')
def log_in():
    return render_template("log_in.html", current_year=datetime.now().year, form=LogForm())


@app.route('/register')
def register():
    return render_template("register.html", current_year=datetime.now().year, form=RegisterForm())


if __name__ == "__main__":
    app.run(debug=True)

# COMMIT CHANGES TO DATABASE
db.session.commit()
