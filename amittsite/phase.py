from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from amittsite.auth import login_required
from amittsite.db import get_db

bp = Blueprint('phase', __name__, url_prefix='/phase')

@bp.route('/')
def index():
    db = get_db()
    phases = db.execute(
        'SELECT p.id, amitt_id, rank, name, summary'
        ' FROM phase p'
        ' ORDER BY amitt_id ASC'
    ).fetchall()
    return render_template('phase/index.html', phases=phases)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        amitt_id = request.form['amitt_id']
        name = request.form['name']
        summary = request.form['summary']
        rank = request.form['rank']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO phase (amitt_id, name, summary, rank)'
                ' VALUES (?, ?, ?, ?)',
                (amitt_id, name, summary, rank)
            )
            db.commit()
            return redirect(url_for('phase.index'))

    return render_template('phase/create.html')


def get_phase(id, check_author=True):
    phase = get_db().execute(
        'SELECT p.id, amitt_id, name, summary, rank'
        ' FROM phase p'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if phase is None:
        abort(404, f"Phase id {id} doesn't exist.")

    return phase

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    phase = get_phase(id)

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
                'UPDATE phase SET name = ?, summary = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('phase.index'))

    return render_template('phase/update.html', phase=phase)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_phase(id)
    db = get_db()
    db.execute('DELETE FROM phase WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('phase.index'))

