from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<title>')
def post(title):
    post = find_post(title)
    return render_template('post.html', d={'post': post})


def find_post(title):
    pass

if __name__ == '__main__':
    app.debug = True
    app.run()