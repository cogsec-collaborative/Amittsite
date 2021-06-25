from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from amittsite.auth import login_required
from amittsite.db import get_db

bp = Blueprint('technique', __name__, url_prefix='/technique')

def get_technique(id, check_author=True):
    technique = get_db().execute(
        'SELECT p.id, p.amitt_id, p.name, p.summary, p.tactic_id'
        ' FROM technique p JOIN tactic u ON p.tactic_id = u.amitt_id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if technique is None:
        abort(404, f"Technique id {id} doesn't exist.")

    return technique

@bp.route('/')
def index():
    db = get_db()
    techniques = db.execute(
        'SELECT p.id, p.amitt_id, p.name, p.summary, p.tactic_id'
        ' FROM technique p JOIN tactic u ON p.tactic_id = u.amitt_id'
        ' ORDER BY p.amitt_id ASC'
    ).fetchall()
    return render_template('technique/index.html', techniques=techniques)


@bp.route('/<int:id>/view', methods=('GET', 'POST'))
def view(id):
    technique = get_technique(id)
    return render_template('technique/view.html', technique=technique)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        amitt_id = request.form['amitt_id']
        name = request.form['name']
        summary = request.form['summary']
        tactic_id = request.form['tactic_id']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO technique (amitt_id, name, summary, tactic_id)'
                ' VALUES (?, ?, ?, ?)',
                (amitt_id, name, summary, tactic_id)
            )
            db.commit()
            return redirect(url_for('technique.index'))

    return render_template('technique/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    technique = get_technique(id)

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
                'UPDATE technique SET name = ?, summary = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('technique.index'))

    return render_template('technique/update.html', technique=technique)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_technique(id)
    db = get_db()
    db.execute('DELETE FROM technique WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('technique.index'))

