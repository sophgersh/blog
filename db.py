import sqlite3

conn = sqlite3.connect('blog.db')
c = conn.cursor()


def find_post(slug):
    query = 'SELECT * FROM blogs WHERE slug = ?'
    posts = c.execute(query, slug)
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

    for query in queries:
        c.execute(query)

    conn.commit()