from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from amittsite.auth import login_required
from amittsite.db import get_db

bp = Blueprint('framework', __name__, url_prefix='/framework')

@bp.route('/')
def index():
    db = get_db()
    frameworks = db.execute(
        'SELECT p.id, amitt_id, name, summary'
        ' FROM framework p'
        ' ORDER BY amitt_id ASC'
    ).fetchall()
    return render_template('framework/index.html', frameworks=frameworks)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        amitt_id = request.form['amitt_id']
        name = request.form['name']
        summary = request.form['summary']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO framework (amitt_id, name, summary)'
                ' VALUES (?, ?, ?)',
                (amitt_id, name, summary)
            )
            db.commit()
            return redirect(url_for('framework.index'))

    return render_template('framework/create.html')


def get_framework(id, check_author=True):
    framework = get_db().execute(
        'SELECT p.id, amitt_id, name, summary'
        ' FROM framework p'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if framework is None:
        abort(404, f"Phase id {id} doesn't exist.")

    return framework

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    framework = get_framework(id)

    if request.method == 'POST':
        name = request.form['name']
        summary = request.form['summary']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE framework SET name = ?, summary = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('framework.index'))

    return render_template('framework/update.html', framework=framework)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_framework(id)
    db = get_db()
    db.execute('DELETE FROM framework WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('framework.index'))

