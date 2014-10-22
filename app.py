from flask import flash, Flask, g, redirect, render_template, request
import db

app = Flask(__name__)
app.secret_key = 'a'

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/blog')
def blog():
    MAX_POSTS = 10
    posts = db.most_recent_posts(MAX_POSTS)
    return render_template('blog.html', d={'posts': posts})

@app.route('/archives')
def archives():
    posts = db.all_posts()
    return render_template('archives.html',d={'posts':posts})

@app.route('/<slug>')
def post(slug):
    post = db.find_post(slug)
    try:
        comments = db.find_comments_for_post(post['id'])
    except:
        comments = ""

    return render_template('post.html', d={'post': post, 'comments': comments})

@app.route('/posts/comment', methods=['POST'])
def comment():
    post = db.find_post(request.form['post_slug'])

    params = {}
    params['post_id'] = post['id']
    params['content'] = request.form['comment']
    params['user'] = request.form['user']

    db.new_comment(params)
    return redirect('/%s' % request.form['post_slug'])


@app.route('/posts/new', methods=['POST'])
def new_post():
    params = {}
    params['title'] = request.form['title']
    params['content'] = request.form['content'].replace("\n", "</p><p>")
    params['username'] = request.form['username']

    post = db.new_post(params)

    if post:
        return redirect('/%s' % post['slug'])
    else:
        flash('Invalid blog post')
        return redirect('/blog')


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == '__main__':
    app.debug = True
    app.run()
