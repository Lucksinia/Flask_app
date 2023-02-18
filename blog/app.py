from flask import Flask

app = Flask(__name__)


@app.route("/")
def index(city="World"):
    return f"<p>Hello, {city}!</p>"
