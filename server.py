from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap

from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import EqualTo, DataRequired

from datetime import datetime

app = Flask(__name__)
Bootstrap(app)
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
    email = StringField(label="email", validators=[DataRequired(),
                                                   validators.Email(message="invalid email address"),
                                                   validators.Length(min=12, message="email too short")])
    password = PasswordField(label="password", validators=[DataRequired(),
                                                           validators.Length(min=8, message="password too short")])
    submit = SubmitField(label="log in")


class RegisterForm(FlaskForm):
    email = StringField(label="email", validators=[DataRequired(),
                                                   validators.Email(message="invalid email address"),
                                                   validators.Length(min=12, message="email too short")])
    password = PasswordField(label="password", validators=[DataRequired(),
                                                           EqualTo('password2', message="passwords must match"),
                                                           validators.Length(min=8, message="password too short")])
    password2 = PasswordField(label="repeat password", validators=[DataRequired(),
                                                                   validators.Length(min=8,
                                                                                     message="password too short")])
    name = StringField(label="name and surname", validators=[DataRequired()])
    street = StringField(label="street", validators=[DataRequired()])
    city = StringField(label="city", validators=[DataRequired()])
    submit = SubmitField(label="log in")


class NewsletterForm(FlaskForm):
    email = StringField(label="email", validators=[validators.Email(message="invalid email address"),
                                                   validators.Length(min=12, message="email too short")])
    submit = SubmitField(label="sign up")


@app.route("/", methods=["GET", "POST"])
def homepage():
    newsletter = NewsletterForm()

    if newsletter.validate_on_submit():
        pass

    return render_template("index.html",
                           current_year=datetime.now().year,
                           newsletter=newsletter)


@app.route("/shop", methods=["GET", "POST"])
def shop():
    newsletter = NewsletterForm()
    items = db.session.query(Item).all()

    search = request.args.get("search")
    gender = request.args.get("gender")
    color = request.args.get("color")
    size = request.args.get("size")
    sort = request.args.get("sort_by")

    if newsletter.validate_on_submit():
        pass

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

    return render_template("shop.html",
                           current_year=datetime.now().year,
                           all_items=items,
                           gender=gender,
                           color=color,
                           size=size,
                           sort=sort,
                           newsletter=newsletter)


@app.route("/shop/<int:item_id>", methods=["GET", "POST"])
def item(item_id):
    newsletter = NewsletterForm()
    item = Item.query.filter_by(id=item_id).first()

    if newsletter.validate_on_submit():
        pass

    return render_template("item.html",
                           current_year=datetime.now().year,
                           item=item,
                           newsletter=newsletter)


@app.route("/about", methods=["GET", "POST"])
def about():
    newsletter = NewsletterForm()

    if newsletter.validate_on_submit():
        pass

    return render_template("about.html",
                           current_year=datetime.now().year,
                           newsletter=newsletter)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    newsletter = NewsletterForm()

    if newsletter.validate_on_submit():
        pass

    return render_template("contact.html",
                           current_year=datetime.now().year,
                           newsletter=newsletter)


@app.route("/log_in", methods=["GET", "POST"])
def log_in():
    form = LogForm()
    newsletter = NewsletterForm()

    if form.validate_on_submit():
        return redirect(url_for("homepage"))

    if newsletter.validate_on_submit():
        pass

    return render_template("log_in.html",
                           current_year=datetime.now().year,
                           form=form,
                           newsletter=newsletter)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    newsletter = NewsletterForm()

    if form.validate_on_submit():
        return redirect(url_for("log_in"))

    if newsletter.validate_on_submit():
        print("xd")

    return render_template("register.html",
                           current_year=datetime.now().year,
                           form=form,
                           newsletter=newsletter)


if __name__ == "__main__":
    app.run(debug=True)

# COMMIT CHANGES TO DATABASE
db.session.commit()
