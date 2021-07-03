from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from amittsite.auth import login_required
from amittsite.database import db_session
from amittsite.models import Metatechnique


bp = Blueprint('metatechnique', __name__, url_prefix='/metatechnique')

def get_metatechnique(id, check_author=True):
    metatechnique = Metatechnique.query.filter(Metatechnique.id == id).first()
    if metatechnique is None:
        abort(404, f"Task id {id} doesn't exist.")
    return metatechnique


@bp.route('/')
def index():
    metatechniques = Metatechnique.query.order_by("amitt_id")
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
            metatechnique = Metatechnique(amitt_id, name, summary)
            db_session.add(metatechnique)
            db_session.commit()
            return redirect(url_for('metatechnique.index'))

    return render_template('metatechnique/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    metatechnique = get_metatechnique(id)

    if request.method == 'POST':
        name = request.form['name']
        summary = request.form['summary']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            metatechnique.name = name
            metatechnique.summary = summary
            db_session.add(metatechnique)
            db_session.commit()            
            return redirect(url_for('metatechnique.index'))

    return render_template('metatechnique/update.html', metatechnique=metatechnique)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    metatechnique = get_metatechnique(id)
    db_session.delete(metatechnique)
    db_session.commit()
    return redirect(url_for('metatechnique.index'))

