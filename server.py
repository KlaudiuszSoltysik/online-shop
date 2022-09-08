from flask import Flask, render_template
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///online_shop.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


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


all_items = db.session.query(Item).all()
db.session.commit()


@app.route('/')
def homepage():
    return render_template("index.html", current_year=datetime.now().year)


@app.route('/shop')
def shop():
    return render_template("shop.html", current_year=datetime.now().year, all_items=all_items)


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
