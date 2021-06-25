from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from amittsite.auth import login_required
from amittsite.db import get_db

bp = Blueprint('tactic', __name__, url_prefix='/tactic')

@bp.route('/')
def index():
    db = get_db()
    tactics = db.execute(
        'SELECT p.id, p.amitt_id, p.rank, p.name, p.summary, p.phase_id'
        ' FROM tactic p JOIN phase u ON p.phase_id = u.amitt_id'
        ' ORDER BY p.amitt_id ASC'
    ).fetchall()
    return render_template('tactic/index.html', tactics=tactics)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        amitt_id = request.form['amitt_id']
        name = request.form['name']
        summary = request.form['summary']
        rank = request.form['rank']
        phase_id = request.form['phase_id']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO tactic (amitt_id, name, summary, rank, phase_id)'
                ' VALUES (?, ?, ?, ?, ?)',
                (amitt_id, name, summary, rank, phase_id)
            )
            db.commit()
            return redirect(url_for('tactic.index'))

    return render_template('tactic/create.html')


def get_tactic(id, check_author=True):
    tactic = get_db().execute(
        'SELECT p.id, p.amitt_id, p.rank, p.name, p.summary, p.phase_id'
        ' FROM tactic p JOIN phase u ON p.phase_id = u.amitt_id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if tactic is None:
        abort(404, f"Phase id {id} doesn't exist.")

    return tactic

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    tactic = get_tactic(id)

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
                'UPDATE tactic SET name = ?, summary = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('tactic.index'))

    return render_template('tactic/update.html', tactic=tactic)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_tactic(id)
    db = get_db()
    db.execute('DELETE FROM tactic WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('tactic.index'))

