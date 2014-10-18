from flask import Flask, render_template

import db

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<slug>')
def post(slug):
    post = db.find_post(slug)
    return render_template('post.html', d={'post': post})

if __name__ == '__main__':
    app.debug = True
    app.run()