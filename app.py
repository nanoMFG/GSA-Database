from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, render_template



# create a Flask application object and set the URI for the database to use
app = Flask(__name__)
app.config["SQLALCEHMY_DATABASE_URI"] = "sqlite:///example.sqlite3"

# creating a database with dummy data
db = SQLAlchemy(app)


@app.route('/')
def hello():
    return 'Hello World'
    
if __name__ == '__main__':
    app.run()