import sqlite3

from flask import g

DATABASE = 'blog.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = _connect_to_database()
    db.row_factory = sqlite3.Row
    return db


def find_post(slug):
    query = 'SELECT * FROM posts WHERE slug = ?'
    posts = get_db().cursor().execute(query, slug)
    return posts.fetchone()


# Use this only to initialize a new database for the first time
def setup():
    queries = [
        '''CREATE TABLE posts (
        id integer primary key,
        title text,
        content text,
        slug text
        )'''
    ]

    db = _connect_to_database()
    c = db.cursor()
    for query in queries:
        c.execute(query)

    db.commit()
    db.close()


def _connect_to_database():
    return sqlite3.connect(DATABASE)