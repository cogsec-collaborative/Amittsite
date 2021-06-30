from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from amittsite.auth import login_required
from amittsite.db import get_db

bp = Blueprint('detection', __name__, url_prefix='/detection')

def get_detection(id, check_author=True):
    db = get_db()
    detection = db.execute(
        'SELECT p.id, p.amitt_id, p.name, p.summary, p.tactic_id'
        ' FROM detection p JOIN tactic u ON p.tactic_id = u.amitt_id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if detection is None:
        abort(404, f"Technique id {id} doesn't exist.")

    techniques = db.execute(
        'SELECT p.detection_id, p.technique_id, p.summary, t.name, t.id'
        ' FROM detection_technique p JOIN technique t ON p.technique_id = t.amitt_id'
        ' WHERE p.detection_id = ?'
        ' ORDER BY p.technique_id ASC',
        (detection['amitt_id'],)
    ).fetchall()

    return (detection, techniques)

@bp.route('/')
def index():
    db = get_db()
    detections = db.execute(
        'SELECT p.id, p.amitt_id, p.name, p.summary, p.tactic_id'
        ' FROM detection p JOIN tactic u ON p.tactic_id = u.amitt_id'
        ' ORDER BY p.amitt_id ASC'
    ).fetchall()
    return render_template('detection/index.html', detections=detections)


@bp.route('/<int:id>/view', methods=('GET', 'POST'))
def view(id):
    detection, techniques = get_detection(id)
    return render_template('detection/view.html', detection=detection, techniques=techniques)


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
                'INSERT INTO detection (amitt_id, name, summary, tactic_id)'
                ' VALUES (?, ?, ?, ?)',
                (amitt_id, name, summary, tactic_id)
            )
            db.commit()
            return redirect(url_for('detection.index'))

    return render_template('detection/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    detection, techniques = get_detection(id)

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
                'UPDATE detection SET name = ?, summary = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('detection.index'))

    return render_template('detection/update.html', detection=detection)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_detection(id)
    db = get_db()
    db.execute('DELETE FROM detection WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('detection.index'))

