DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS phase;
DROP TABLE IF EXISTS tactic;
DROP TABLE IF EXISTS framework;
DROP TABLE IF EXISTS task;
DROP TABLE IF EXISTS technique;
DROP TABLE IF EXISTS counter;
DROP TABLE IF EXISTS sector;
DROP TABLE IF EXISTS metatechnique;
DROP TABLE IF EXISTS reference;
DROP TABLE IF EXISTS dataset;
DROP TABLE IF EXISTS actor_type;
DROP TABLE IF EXISTS incident;
DROP TABLE IF EXISTS response_type;
DROP TABLE IF EXISTS playbook;
DROP TABLE IF EXISTS techniques_counters;


CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE phase (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  amitt_id TEXT NOT NULL,
  rank INTEGER NOT NULL,
  name TEXT NOT NULL,
  summary TEXT NOT NULL
);

CREATE TABLE tactic (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  amitt_id TEXT NOT NULL,
  phase_id TEXT NOT NULL,
  rank INTEGER NOT NULL,
  name TEXT NOT NULL,
  summary TEXT NOT NULL,
  FOREIGN KEY (phase_id) REFERENCES phase (amitt_id)
);

CREATE TABLE framework (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  amitt_id TEXT NOT NULL,
  name TEXT NOT NULL,
  summary TEXT NOT NULL
);

CREATE TABLE task (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  amitt_id TEXT NOT NULL,
  tactic_id TEXT NOT NULL,
  framework_id TEXT NOT NULL,
  name TEXT NOT NULL,
  summary TEXT NOT NULL,
  FOREIGN KEY (phase_id) REFERENCES phase (amitt_id),
  FOREIGN KEY (framework_id) REFERENCES framework (amitt_id)
);

CREATE TABLE technique (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  amitt_id TEXT NOT NULL,
  tactic_id TEXT NOT NULL,
  name TEXT NOT NULL,
  summary TEXT NOT NULL,
  FOREIGN KEY (tactic_id) REFERENCES tactic (amitt_id)
);

CREATE TABLE counter (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  amitt_id TEXT NOT NULL,
  metatechnique_id TEXT NOT NULL,
  tactic_id TEXT NOT NULL,
  name TEXT NOT NULL,
  summary TEXT NOT NULL,
  FOREIGN KEY (metatechnique_id) REFERENCES metatechnique (amitt_id),
  FOREIGN KEY (tactic_id) REFERENCES tactic (amitt_id)
);

/* CREATE TABLE sector (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  amitt_id TEXT NOT NULL,
  name TEXT NOT NULL,
  summary TEXT NOT NULL
); */

CREATE TABLE metatechnique (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  amitt_id TEXT NOT NULL,
  name TEXT NOT NULL,
  summary TEXT NOT NULL
);

/* CREATE TABLE reference (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  amitt_id TEXT NOT NULL,
  name TEXT NOT NULL,
  summary TEXT NOT NULL
);

CREATE TABLE dataset (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  amitt_id TEXT NOT NULL,
  name TEXT NOT NULL,
  summary TEXT NOT NULL
);

CREATE TABLE actor_type (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  amitt_id TEXT NOT NULL,
  sector_id TEXT NOT NULL,
  framework_id TEXT NOT NULL,
  name TEXT NOT NULL,
  summary TEXT NOT NULL,
  FOREIGN KEY (sector_id) REFERENCES sector (amitt_id),
  FOREIGN KEY (framework_id) REFERENCES framework (amitt_id)
);

CREATE TABLE incident (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  amitt_id TEXT NOT NULL,
  name TEXT NOT NULL,
  summary TEXT NOT NULL,
  incident_type TEXT NOT NULL,
  year_started INTEGER NOT NULL,
  countries TEXT NOT NULL,
  found_via TEXT NOT NULL
);

CREATE TABLE response_type (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  amitt_id TEXT NOT NULL,
  name TEXT NOT NULL,
  summary TEXT NOT NULL
);

CREATE TABLE playbook (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  object_type TEXT NOT NULL,
  object_id TEXT NOT NULL,
  summary TEXT NOT NULL
);

CREATE TABLE techniques_counters (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  technique_id TEXT NOT NULL,
  counter_id TEXT NOT NULL,
  summary TEXT NOT NULL,
  FOREIGN KEY (technique_id) REFERENCES technique (amitt_id),
  FOREIGN KEY (counter_id) REFERENCES counter (amitt_id)
);
*/





