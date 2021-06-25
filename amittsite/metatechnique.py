from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from amittsite.auth import login_required
from amittsite.db import get_db

bp = Blueprint('metatechnique', __name__, url_prefix='/metatechnique')

def get_metatechnique(id, check_author=True):
    metatechnique = get_db().execute(
        'SELECT p.id, p.amitt_id, p.name, p.summary'
        ' FROM metatechnique p'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if metatechnique is None:
        abort(404, f"Task id {id} doesn't exist.")

    return metatechnique

@bp.route('/')
def index():
    db = get_db()
    metatechniques = db.execute(
        'SELECT p.id, p.amitt_id, p.name, p.summary'
        ' FROM metatechnique p'
        ' ORDER BY p.amitt_id ASC'
    ).fetchall()
    return render_template('metatechnique/index.html', metatechniques=metatechniques)


@bp.route('/<int:id>/view', methods=('GET', 'POST'))
def view(id):
    metatechnique = get_metatechnique(id)
    return render_template('metatechnique/view.html', metatechnique=metatechnique)


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
                'INSERT INTO metatechnique (amitt_id, name, summary)'
                ' VALUES (?, ?, ?)',
                (amitt_id, name, summary)
            )
            db.commit()
            return redirect(url_for('metatechnique.index'))

    return render_template('metatechnique/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    metatechnique = get_metatechnique(id)

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
                'UPDATE metatechnique SET name = ?, summary = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('metatechnique.index'))

    return render_template('metatechnique/update.html', metatechnique=metatechnique)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_metatechnique(id)
    db = get_db()
    db.execute('DELETE FROM metatechnique WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('metatechnique.index'))

