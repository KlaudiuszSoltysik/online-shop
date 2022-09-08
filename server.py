from flask import Flask, render_template, request
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

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

    return render_template("shop.html", current_year=datetime.now().year, all_items=items)


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


if __name__ == "__main__":
    app.run(debug=True)

# COMMIT CHANGES TO DATABASE
db.session.commit()
