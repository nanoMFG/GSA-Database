from flask import Blueprint
from src.grdb.database.models import Author, Recipe

from server import research_db

index = Blueprint('index', __name__, url_prefix='/')


@index.route('/hello')
def hello():
    print(research_db)
    a = Author.query.filter(Author.id < 10)
    b = research_db.session.query(Author).filter(Author.id < 10)
    s = ''
    for author in a:
        s += str(author.first_name) + " "
    for author in b:
        s += str(author.first_name) + " "
    research_db.session.close()
    return s
