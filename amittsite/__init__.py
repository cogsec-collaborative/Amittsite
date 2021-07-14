import os

from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from amittsite.database import init_db
from amittsite.database import db_session
from . import auth
from . import counter
from . import detection
from . import example
from . import framework
from . import group
from . import incident
from . import metatechnique
from . import phase
from . import resource
from . import responsetype
from . import tactic
from . import task
from . import technique
from . import tool
import sqlite3


def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Configuration settings
    # app.config.from_mapping(
    #     SECRET_KEY=os.environ.get('SECRET_KEY') or 'dev',
    #     DATABASE=os.path.join(app.instance_path, 'amittsite.sqlite'),
    #     SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'amittsite.sqlite'),
    # )
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY') or 'dev',
        SQLALCHEMY_DATABASE_URI=os.environ['DATABASE_URL2'],
    )
    print('{}'.format(app.config))

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Main route: to index page
    @app.route('/')
    def index():
        return render_template('index.html')

    # About page
    @app.route('/about')
    def about():
        return render_template('about.html')

    # Testing route: a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/textgrid')
    def textgrid():
        array = [
          ['TA01', 'TA02', 'TA03', 'TA04', 'TA05', 'TA06', 'TA07', 'TA08', 'TA09', 'TA10', 'TA11', 'TA12'],
          ['T0001', 'T0005', 'T0007', 'T0010', 'T0016', 'T0019', 'T0029', 'T0039', 'T0047', 'T0057', 'T0058', 'T0062'],
          ['T0002', 'T0006', 'T0008', 'T0011', 'T0017', 'T0020', 'T0030', 'T0040', 'T0048', 'T0061', 'T0059', 'T0063'],
          ['T0003', '', 'T0009', 'T0012', 'T0018', 'T0021', 'T0031', 'T0041', 'T0049', '', 'T0060', 'T0064'],
          ['T0004', '', '', 'T0013', '', 'T0022', 'T0032', 'T0042', 'T0050', '', '', ''],
          ['', '', '', 'T0014', '', 'T0023', 'T0033', 'T0043', 'T0051', '', '', ''],
          ['', '', '', 'T0015', '', 'T0024', 'T0034', 'T0044', 'T0052', '', '', ''],
          ['', '', '', '', '', 'T0025', 'T0035', 'T0045', 'T0053', '', '', ''],
          ['', '', '', '', '', 'T0026', 'T0036', 'T0046', 'T0054', '', '', ''],
          ['', '', '', '', '', 'T0027', 'T0037', '', 'T0055', '', '', ''],
          ['', '', '', '', '', 'T0028', 'T0038', '', 'X0056', '', '', '']
          ]
        return render_template('textgrid.html', gridparams=["#redgrid", '#E74C3C', array])#'#E74C3C')


    @app.route('/mapblobs')
    def mapblobs():
        array = []
        return render_template('mapblobs.html', array=array)


    # do the database stuff
    init_db()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    # register all the object code
    app.register_blueprint(auth.bp)
    app.register_blueprint(counter.bp)
    app.register_blueprint(detection.bp)
    app.register_blueprint(example.bp)
    app.register_blueprint(framework.bp)
    app.register_blueprint(group.bp)
    app.register_blueprint(incident.bp)
    app.register_blueprint(metatechnique.bp)
    app.register_blueprint(phase.bp)
    app.register_blueprint(resource.bp)
    app.register_blueprint(responsetype.bp)
    app.register_blueprint(tactic.bp)
    app.register_blueprint(task.bp)
    app.register_blueprint(technique.bp)
    app.register_blueprint(tool.bp)
    app.add_url_rule('/', endpoint='index')

    return app
