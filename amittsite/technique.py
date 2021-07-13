from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
import pandas as pd

from amittsite.auth import login_required
from amittsite.database import db_session
from amittsite.models import Technique
from amittsite.models import Tactic
from amittsite.models import Counter
from amittsite.models import CounterTechnique
from amittsite.models import Detection
from amittsite.models import DetectionTechnique


bp = Blueprint('technique', __name__, url_prefix='/technique')

def get_technique(id, check_author=True):
    technique = Technique.query.join(Tactic).filter(Technique.id == id).first()
    if technique is None:
        abort(404, f"Technique id {id} doesn't exist.")
    counters = Counter.query.join(CounterTechnique).filter(CounterTechnique.technique_id == technique.amitt_id).order_by("amitt_id")
    detections = Detection.query.join(DetectionTechnique).filter(DetectionTechnique.technique_id == technique.amitt_id).order_by("amitt_id")
    return (technique, counters, detections)

@bp.route('/')
def index():
    techniques = Technique.query.join(Tactic).order_by("amitt_id")

    # Create grid for clickable visualisation
    df = pd.read_sql(techniques.statement, techniques.session.bind)
    dflists = df.groupby('tactic_id')['amitt_id'].apply(list).reset_index()
    dfidgrid = pd.DataFrame(dflists['amitt_id'].to_list())
    dfgrid = pd.concat([dflists[['tactic_id']], dfidgrid], axis=1).fillna('')
    gridarray = [dfgrid[col].to_list() for col in dfgrid.columns]

    return render_template('technique/index.html', techniques=techniques, gridparams=["#redgrid", '#E74C3C', gridarray])


@bp.route('/<int:id>/view', methods=('GET', 'POST'))
def view(id):
    technique, counters, detections = get_technique(id)
    return render_template('technique/view.html', technique=technique, counters=counters, detections=detections)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        amitt_id = request.form['amitt_id']
        tactic_id = request.form['tactic_id']
        name = request.form['name']
        summary = request.form['summary']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            technique = Technique(amitt_id, tactic_id, name, summary)
            db_session.add(technique)
            db_session.commit()
            return redirect(url_for('technique.index'))

    return render_template('technique/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    technique, counters, detections = get_technique(id)

    if request.method == 'POST':
        name = request.form['name']
        summary = request.form['summary']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            technique.name = name
            technique.summary = summary
            db_session.add(technique)
            db_session.commit()
            return redirect(url_for('technique.index'))

    return render_template('technique/update.html', technique=technique)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    technique, counters, detections = get_technique(id)
    db_session.delete(technique)
    db_session.commit()
    return redirect(url_for('technique.index'))

