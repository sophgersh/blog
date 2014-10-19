from flask import flash, Flask, g, redirect, render_template, request
from slugify import slugify
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
  
    comment = db.find_comments(slug)
    r={'post':post}
    
    return render_template('post.html', d={'post': post},c={'comment':comment})

@app.route('/posts/comment',methods=['POST'])
def comment():
    params={}
    
    params['Title']=slugify(request.form['Title'])
    params['content']=request.form['comment'].replace("\n","</p><p>")
   
    slug = db.post_comments(params)
    return redirect ('/%s' % slug )   
    
    
    
@app.route('/posts/new', methods=['POST'])
def new_post():
	params = {}
	params['title'] = request.form['title']
	params['content'] = request.form['content'].replace("\n","</p><p>")

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
