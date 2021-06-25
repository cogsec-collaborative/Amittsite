from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from amittsite.auth import login_required
from amittsite.db import get_db

bp = Blueprint('task', __name__, url_prefix='/task')

def get_task(id, check_author=True):
    task = get_db().execute(
        'SELECT p.id, p.amitt_id, p.name, p.summary, p.tactic_id, p.framework_id'
        ' FROM task p JOIN tactic u ON p.tactic_id = u.amitt_id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if task is None:
        abort(404, f"Task id {id} doesn't exist.")

    return task

@bp.route('/')
def index():
    db = get_db()
    tasks = db.execute(
        'SELECT p.id, p.amitt_id, p.name, p.summary, p.tactic_id, p.framework_id'
        ' FROM task p JOIN tactic u ON p.tactic_id = u.amitt_id'
        ' ORDER BY p.amitt_id ASC'
    ).fetchall()
    return render_template('task/index.html', tasks=tasks)


@bp.route('/<int:id>/view', methods=('GET', 'POST'))
def view(id):
    task = get_task(id)
    return render_template('task/view.html', task=task)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        amitt_id = request.form['amitt_id']
        name = request.form['name']
        summary = request.form['summary']
        tactic_id = request.form['tactic_id']
        framework_id = request.form['framework_id']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO task (amitt_id, name, summary, tactic_id, framework_id)'
                ' VALUES (?, ?, ?, ?, ?)',
                (amitt_id, name, summary, tactic_id, framework_id)
            )
            db.commit()
            return redirect(url_for('task.index'))

    return render_template('task/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    task = get_task(id)

    if request.method == 'POST':
        title = request.form['name']
        body = request.form['summary']
        error = None

        if not title:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE task SET name = ?, summary = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('task.index'))

    return render_template('task/update.html', task=task)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_task(id)
    db = get_db()
    db.execute('DELETE FROM task WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('task.index'))

