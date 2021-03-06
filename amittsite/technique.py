from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
import pandas as pd

from amittsite.auth import login_required
from amittsite.database import db_session
from amittsite.models import Technique
from amittsite.models import Example
from amittsite.models import Tactic
from amittsite.models import Counter
from amittsite.models import CounterTechnique
from amittsite.models import Detection
from amittsite.models import DetectionTechnique
from amittsite.models import IncidentTechnique


bp = Blueprint('technique', __name__, url_prefix='/technique')

def get_technique(id, check_author=True):
    technique = Technique.query.join(Tactic).filter(Technique.id == id).first()
    if technique is None:
        abort(404, f"Technique id {id} doesn't exist.")
    examples = Example.query.filter(Example.object_id == technique.amitt_id).order_by("amitt_id")
    counters = Counter.query.join(CounterTechnique).filter(CounterTechnique.technique_id == technique.amitt_id).order_by("amitt_id")
    detections = Detection.query.join(DetectionTechnique).filter(DetectionTechnique.technique_id == technique.amitt_id).order_by("amitt_id")
    incidents = IncidentTechnique.query.filter(IncidentTechnique.technique_id == technique.amitt_id).order_by("incident_id")
    return (technique, examples, counters, detections, incidents)


def create_technique_grid():
    techniques = Technique.query.join(Tactic).order_by("amitt_id")

    # Create grid for clickable visualisation
    df = pd.read_sql(techniques.statement, techniques.session.bind)
    dflists = df.groupby('tactic_id')['amitt_id'].apply(list).reset_index()
    dfidgrid = pd.DataFrame(dflists['amitt_id'].to_list())
    dfgrid = pd.concat([dflists[['tactic_id']], dfidgrid], axis=1).fillna('')
    techniques_grid = [dfgrid[col].to_list() for col in dfgrid.columns]

    # Create dict for use in visualisation and list updates
    df.index = df.amitt_id
    technique_names = df[['name']].transpose().to_dict('records')[0]

    return techniques, techniques_grid, technique_names


@bp.route('/')
def index():
    techniques, techgrid, technames = create_technique_grid()

    return render_template('technique/index.html', techniques=techniques, 
        gridparams=["#redgrid", '#E74C3C', techgrid, technames])



@bp.route('/<int:id>/view', methods=('GET', 'POST'))
def view(id):
    technique, examples, counters, detections, incidents = get_technique(id)
    return render_template('technique/view.html', technique=technique, examples=examples, counters=counters, 
        detections=detections, incidents=incidents)


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
    technique, examples, counters, detections, incidents = get_technique(id)

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
    technique, examples, counters, detections, incidents = get_technique(id)
    db_session.delete(technique)
    db_session.commit()
    return redirect(url_for('technique.index'))

