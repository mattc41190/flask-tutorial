from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)

def get_post(id, check_author=True):
    db = get_db()
    query = (
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?'
    )
    post = db.execute(query, (id,)).fetchone()

    if post is None:
        abort(404, "Post id {0} not found".format(id))
    if check_author and post['author_id'] != g.user['id']:
        abort(403)
    
    return post


@bp.route('/')
def index():
    db = get_db()
    query = ('SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC')
    posts = db.execute(query).fetchall()

    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    user_id = g.user['id']

    print(request.method)

    if request.method == 'POST':
        title = request.form['title']
        body  = request.form['body']
        error = None

        if not title:
            error = 'title is required'
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            sql_stmt = (
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?,?,?)'
            )
            db.execute(sql_stmt, (title, body, user_id))
            db.commit()
            return redirect(url_for('blog.index'))
        
    return render_template('blog/create.html')

@bp.route('/<int:id>/update', methods=['GET', 'POST'])
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error =  'Title is required.'
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            sql_stmt = (
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?'
            )
            db.execute(sql_stmt, (title, body, id))
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    sql_stmt = (
        'DELETE FROM post WHERE id = ?'
    )
    db.execute(sql_stmt, (id,))
    db.commit()
    return redirect(url_for('blog.index'))
