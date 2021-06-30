import os

from flask import Flask
from flask import render_template
from . import db
from . import auth
from . import counter
from . import detection
from . import framework
from . import metatechnique
from . import phase
from . import tactic
from . import task
from . import technique
import sqlite3


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'amittsite.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # root? 
    @app.route('/')
    def index():
        return render_template('index.html')

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    db.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(counter.bp)
    app.register_blueprint(detection.bp)
    app.register_blueprint(framework.bp)
    app.register_blueprint(metatechnique.bp)
    app.register_blueprint(phase.bp)
    app.register_blueprint(tactic.bp)
    app.register_blueprint(task.bp)
    app.register_blueprint(technique.bp)
    app.add_url_rule('/', endpoint='index')


    # Load up database
    # olddb = sqlite3.connect('amitt_sqlite.db')
    # oldcursor = olddb.execute('SELECT name FROM sqlite_master WHERE type = "table"')
    # print('tables: ')
    # for row in oldcursor:
    #     print('{}'.format(row))

    # # phases
    # oldcursor = olddb.execute("SELECT id, name, rank, summary from df_phases")
    # for row in oldcursor:
    #     db.execute(
    #         'INSERT INTO phase (row[0], row[1], row[2], row[3])'
    #         ' VALUES (?, ?, ?, ?)',
    #         (amitt_id, name, summary, rank)
    #     )

    # db.commit()


    return app
