from sqlalchemy import Column, Integer, String, Text, ForeignKey
from amittsite.database import Base


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(120))

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User {self.username!r}>'


class Phase(Base):
    __tablename__ = 'phase'
    id = Column(Integer, primary_key=True)
    amitt_id = Column(String(20), unique=True)
    rank = Column(Integer)
    name = Column(String(200))
    summary = Column(Text)

    def __init__(self, amitt_id=None, rank=None, name=None, summary=None):
        self.amitt_id = amitt_id
        self.rank = rank
        self.name = name
        self.summary = summary

    def __repr__(self):
        return f'<Phase {self.amitt_id!r} {self.name!r}>'


class Tactic(Base):
    __tablename__ = 'tactic'
    id = Column(Integer, primary_key=True)
    amitt_id = Column(String(20), unique=True)
    phase_id = Column(String(20), ForeignKey('phase.amitt_id'))
    rank = Column(Integer)
    name = Column(String(200))
    summary = Column(Text)

    def __init__(self, amitt_id=None, phase_id=None, 
        rank=None, name=None, summary=None):
        self.amitt_id = amitt_id
        self.phase_id = phase_id
        self.rank = rank
        self.name = name
        self.summary = summary

    def __repr__(self):
        return f'<Tactic {self.amitt_id!r} {self.name!r}>'


class Framework(Base):
    __tablename__ = 'framework'
    id = Column(Integer, primary_key=True)
    amitt_id = Column(String(20), unique=True)
    name = Column(String(200))
    summary = Column(Text)

    def __init__(self, amitt_id=None, name=None, summary=None):
        self.amitt_id = amitt_id
        self.name = name
        self.summary = summary

    def __repr__(self):
        return f'<Framework {self.amitt_id!r} {self.name!r}>'


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    amitt_id = Column(String(20), unique=True)
    tactic_id = Column(String(20), ForeignKey('tactic.amitt_id'))
    framework_id = Column(String(20), ForeignKey('framework.amitt_id'))
    name = Column(String(200))
    summary = Column(Text)

    def __init__(self, amitt_id=None, tactic_id=None, framework_id=None, 
        name=None, summary=None):
        self.amitt_id = amitt_id
        self.tactic_id = tactic_id
        self.framework_id = framework_id
        self.name = name
        self.summary = summary

    def __repr__(self):
        return f'<Task {self.amitt_id!r} {self.name!r}>'


class Technique(Base):
    __tablename__ = 'technique'
    id = Column(Integer, primary_key=True)
    amitt_id = Column(String(20), unique=True)
    tactic_id = Column(String(20), ForeignKey('tactic.amitt_id'))
    name = Column(String(200))
    summary = Column(Text)

    def __init__(self, amitt_id=None, tactic_id=None, 
        name=None, summary=None):
        self.amitt_id = amitt_id
        self.tactic_id = tactic_id
        self.name = name
        self.summary = summary

    def __repr__(self):
        return f'<Technique {self.amitt_id!r} {self.name!r}>'


class Counter(Base):
    __tablename__ = 'counter'
    id = Column(Integer, primary_key=True)
    amitt_id = Column(String(20), unique=True)
    metatechnique_id = Column(String(20), unique=True)
    tactic_id = Column(String(20), ForeignKey('tactic.amitt_id'))
    name = Column(String(200))
    summary = Column(Text)

    def __init__(self, amitt_id=None, metatechnique_id=None, tactic_id=None, 
        name=None, summary=None):
        self.amitt_id = amitt_id
        self.metatechnique_id = metatechnique_id
        self.tactic_id = tactic_id
        self.name = name
        self.summary = summary

    def __repr__(self):
        return f'<Counter {self.amitt_id!r} {self.name!r}>'


class Detection(Base):
    __tablename__ = 'detection'
    id = Column(Integer, primary_key=True)
    amitt_id = Column(String(20), unique=True)
    tactic_id = Column(String(20), ForeignKey('tactic.amitt_id'))
    name = Column(String(200))
    summary = Column(Text)

    def __init__(self, amitt_id=None, tactic_id=None, name=None, summary=None):
        self.amitt_id = amitt_id
        self.tactic_id = tactic_id
        self.name = name
        self.summary = summary

    def __repr__(self):
        return f'<Counter {self.amitt_id!r} {self.name!r}>'


class Metatechnique(Base):
    __tablename__ = 'metatechnique'
    id = Column(Integer, primary_key=True)
    amitt_id = Column(String(20), unique=True)
    name = Column(String(200))
    summary = Column(Text)

    def __init__(self, amitt_id=None, name=None, summary=None):
        self.amitt_id = amitt_id
        self.name = name
        self.summary = summary

    def __repr__(self):
        return f'<Metatechnique {self.amitt_id!r} {self.name!r}>'


class CounterTactic(Base):
    __tablename__ = 'counter_tactic'
    id = Column(Integer, primary_key=True)
    counter_id = Column(String(20), ForeignKey('counter.amitt_id'))
    tactic_id = Column(String(20), ForeignKey('tactic.amitt_id'))
    main_tactic = Column(String(3))
    summary = Column(Text)

    def __init__(self, counter_id=None, tactic_id=None, 
        main_tactic=None, summary=None):
        self.counter_id = counter_id
        self.tactic_id = tactic_id
        self.main_tactic = main_tactic
        self.summary = summary

    def __repr__(self):
        return f'<CounterTactic {self.counter_id!r} {self.tactic_id!r}>'


class CounterTechnique(Base):
    __tablename__ = 'counter_technique'
    id = Column(Integer, primary_key=True)
    counter_id = Column(String(20), ForeignKey('counter.amitt_id'))
    technique_id = Column(String(20), ForeignKey('technique.amitt_id'))
    summary = Column(Text)

    def __init__(self, counter_id=None, technique_id=None, summary=None):
        self.counter_id = counter_id
        self.technique_id = technique_id
        self.summary = summary

    def __repr__(self):
        return f'<CounterTechnique {self.counter_id!r} {self.technique_id!r}>'


class DetectionTechnique(Base):
    __tablename__ = 'detection_technique'
    id = Column(Integer, primary_key=True)
    detection_id = Column(String(20), ForeignKey('detection.amitt_id'))
    technique_id = Column(String(20), ForeignKey('technique.amitt_id'))
    summary = Column(Text)

    def __init__(self, detection_id=None, technique_id=None, summary=None):
        self.detection_id = detection_id
        self.technique_id = technique_id
        self.summary = summary

    def __repr__(self):
        return f'<CDetectionTechnique {self.detection_id!r} {self.technique_id!r}>'

'''
/* CREATE TABLE IF NOT EXISTS sector (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  amitt_id TEXT NOT NULL,
  name TEXT NOT NULL,
  summary TEXT NOT NULL
); */

/* CREATE TABLE IF NOT EXISTS reference (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  amitt_id TEXT NOT NULL,
  name TEXT NOT NULL,
  summary TEXT NOT NULL
); */

/* CREATE TABLE IF NOT EXISTS dataset (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  amitt_id TEXT NOT NULL,
  name TEXT NOT NULL,
  summary TEXT NOT NULL
);*/

/* CREATE TABLE IF NOT EXISTS actor_type (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  amitt_id TEXT NOT NULL,
  sector_id TEXT NOT NULL,
  framework_id TEXT NOT NULL,
  name TEXT NOT NULL,
  summary TEXT NOT NULL,
  FOREIGN KEY (sector_id) REFERENCES sector (amitt_id),
  FOREIGN KEY (framework_id) REFERENCES framework (amitt_id)
); */

/* CREATE TABLE IF NOT EXISTS incident (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  amitt_id TEXT NOT NULL,
  name TEXT NOT NULL,
  summary TEXT NOT NULL,
  incident_type TEXT NOT NULL,
  year_started INTEGER NOT NULL,
  countries TEXT NOT NULL,
  found_via TEXT NOT NULL
); */

/* CREATE TABLE IF NOT EXISTS response_type (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  amitt_id TEXT NOT NULL,
  name TEXT NOT NULL,
  summary TEXT NOT NULL
);*/

/* CREATE TABLE IF NOT EXISTS playbook (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  object_type TEXT NOT NULL,
  object_id TEXT NOT NULL,
  summary TEXT NOT NULL
);*/
'''
