from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from amittsite.auth import login_required
from amittsite.db import get_db

bp = Blueprint('counter', __name__, url_prefix='/counter')

def get_counter(id, check_author=True):
    db = get_db()
    counter = db.execute(
        'SELECT p.id, p.amitt_id, p.name, p.summary, p.tactic_id'
        ' FROM counter p JOIN tactic u ON p.tactic_id = u.amitt_id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if counter is None:
        abort(404, f"Technique id {id} doesn't exist.")

    techniques = db.execute(
        'SELECT p.counter_id, p.technique_id, p.summary, t.name, t.id'
        ' FROM counter_technique p JOIN technique t ON p.technique_id = t.amitt_id'
        ' WHERE p.counter_id = ?'
        ' ORDER BY p.technique_id ASC',
        (counter['amitt_id'],)
    ).fetchall()

    return (counter, techniques)

@bp.route('/')
def index():
    db = get_db()
    counters = db.execute(
        'SELECT p.id, p.amitt_id, p.name, p.summary, p.tactic_id, p.metatechnique_id'
        ' FROM counter p JOIN tactic u ON p.tactic_id = u.amitt_id'
        ' ORDER BY p.amitt_id ASC'
    ).fetchall()
    return render_template('counter/index.html', counters=counters)


@bp.route('/<int:id>/view', methods=('GET', 'POST'))
def view(id):
    counter, techniques = get_counter(id)
    return render_template('counter/view.html', counter=counter, techniques=techniques)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        amitt_id = request.form['amitt_id']
        name = request.form['name']
        summary = request.form['summary']
        tactic_id = request.form['tactic_id']
        metatechnique_id = request.form['metatechnique_id']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO counter (amitt_id, name, summary, tactic_id, metatechnique_id)'
                ' VALUES (?, ?, ?, ?, ?)',
                (amitt_id, name, summary, tactic_id, metatechnique_id)
            )
            db.commit()
            return redirect(url_for('counter.index'))

    return render_template('counter/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    counter, techniques = get_counter(id)

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
                'UPDATE counter SET name = ?, summary = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('counter.index'))

    return render_template('counter/update.html', counter=counter)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_counter(id)
    db = get_db()
    db.execute('DELETE FROM counter WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('counter.index'))

