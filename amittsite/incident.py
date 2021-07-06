from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from amittsite.auth import login_required
from amittsite.database import db_session
from amittsite.models import Incident


bp = Blueprint('incident', __name__, url_prefix='/incident')

def get_incident(id, check_author=True):
    incident = Incident.query.filter(Incident.id == id).first()
    if incident is None:
        abort(404, f"Incident id {id} doesn't exist.")
    return incident


@bp.route('/')
def index():
    incidents = Incident.query.all() #.order_by("amitt_id")
    return render_template('incident/index.html', incidents=incidents)


@bp.route('/<int:id>/view', methods=('GET', 'POST'))
def view(id):
    incident = get_incident(id)
    return render_template('incident/view.html', incident=incident)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        amitt_id = request.form['amitt_id']
        name = request.form['name']
        summary = request.form['summary']
        #FIXIT add other variables
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            incident = Incident(amitt_id, name, summary)
            db_session.add(incident)
            db_session.commit()
            return redirect(url_for('incident.index'))

    return render_template('incident/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    incident = get_incident(id)

    if request.method == 'POST':
        name = request.form['name']
        summary = request.form['summary']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            incident.name = name
            incident.summary = summary
            db_session.add(incident)
            db_session.commit()            
            return redirect(url_for('incident.index'))

    return render_template('incident/update.html', incident=incident)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    incident = get_incident(id)
    db_session.delete(incident)
    db_session.commit()            
    return redirect(url_for('incident.index'))

