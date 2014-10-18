from flask import flash, Flask, g, redirect, render_template, request

import db

app = Flask(__name__)
app.secret_key = 'a'


@app.route('/')
def index():
    MAX_POSTS = 10
    posts = db.most_recent_posts(MAX_POSTS)
    return render_template('index.html', d={'posts': posts})


@app.route('/<slug>')
def post(slug):
    post = db.find_post(slug)
    return render_template('post.html', d={'post': post})


@app.route('/posts/new', methods=['POST'])
def new_post():
    params = {}
    params['title'] = request.form['title']
    params['content'] = request.form['content']

    post = db.new_post(params)

    if post:
        return redirect('/%s' % post['slug'])
    else:
        flash('Invalid blog post')
        return redirect('/')


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == '__main__':
    app.debug = True
    app.run()