from flask import Flask, render_template
from datetime import datetime


app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template("index.html", current_year=datetime.now().year)


@app.route('/shop')
def shop():
    return render_template("shop.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
