import traceback

from flask import Flask, render_template
from data.db_data import db_session
from data.db_data.models.users import User
from data.db_data.models.posts import Posts


app = Flask(__name__)
app.secret_key = "tgNews"


@app.route('/')
def indexMain():
    db = db_session.create_session()
    dataPost = []
    for post in db.query(Posts).all():
        dataPost.append((post.id, post.namePost, post.descPost))
    db.close()

    return render_template('index.html', item=dataPost)


@app.route('/form_create')
def formCreate():
    return render_template('form_create.html')


@app.route('/posts/<id_post>')
def openPostId(id_post):
    db = db_session.create_session()
    post = db.query(Posts).filter(Posts.id == id_post).first()
    db.close()

    return render_template(f'posts/{id_post}.html', post=post.namePost)

if __name__ == '__main__':
    db_session.global_init('data/db_data/db/dbTg.db')
    context = ('cert.pem', 'key.pem')
    app.run(debug=True, ssl_context=context)
