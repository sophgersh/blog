import sqlite3

from flask import g
from slugify import slugify



DATABASE = 'blog.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = _connect_to_database()
        db.row_factory = sqlite3.Row
    return db


def new_post(params):
    query = "INSERT INTO posts (title, content, slug) VALUES (:title, :content, :slug)"

    slug = slugify(params['title'])
    params['slug'] = slug

    try:
        with get_db() as db:
            db.cursor().execute(query, params)
            db.commit()
    except sqlite3.IntegrityError:
        return None

    return find_post(slug)


def find_post(slug):
    query = 'SELECT * FROM posts WHERE slug = ? LIMIT 1'
    posts = get_db().execute(query, (slug,))
    return posts.fetchone()
def most_recent_posts(n):
    query = 'SELECT * FROM posts ORDER BY id DESC LIMIT ?'
    posts = get_db().execute(query, (n,))
    return posts
def post_comments(params):
    query= "INSERT INTO comments(slug,content) VALUES(:Title,:content)"
    get_db().execute(query, params)
    get_db().commit()
    
    return params['Title']

def find_comments(title):
    query= 'SELECT content FROM comments WHERE slug == ?'
    posts = get_db().execute(query, (title,))
    
    return  posts.fetchall() 
# Use this only to initialize a new database for the first time
def setup():
    queries = [
        '''CREATE TABLE posts (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        slug TEXT UNIQUE NOT NULL
        )''','''CREATE TABLE comments (
        id INTEGER PRIMARY KEY,
        slug TEXT NOT NULL,
        content TEXT NOT NULL
        )'''
    ]
    
    db = _connect_to_database()
    for query in queries:
        db.execute(query)
    
       

    db.commit()
    db.close()


def _connect_to_database():
    return sqlite3.connect(DATABASE)
