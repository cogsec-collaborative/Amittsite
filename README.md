# Amittsite
Amitt website code - makes AMITT framework objects accessible to non-technical people.  

Written in Python, Flask, D3.  

Running locally - getting set up

* install postgresql locally https://www.postgresql.org/
* Use the AMITT repo to generate a database for you https://github.com/cogsec-collaborative/AMITT file HTML_GENERATING_CODE/AMITT_create_website_sql.ipynb will do this for you (run it using jupyter - install that using anaconda https://www.anaconda.com/)
* Open a terminal window.  git clone this repo. cd into it   

Running locally

* . venv/bin/activate; 
* export FLASK_APP=amittsite; export FLASK_ENV=development; export DATABASE_URL2="postgresql:///amittsite"
* flask run
* go to http://127.0.0.1:5000/


Running on Heroku - getting set up

* Create a heroku account. Create an app. 
* Click on the app, then the resources tab. Add the Postgres add-on.  
* go to https://dashboard.heroku.com/apps/<your heroku app name>/settings
* click "reveal config vars"
* Edit DATABASE_URL: take a copy of it. It will start with "postgres://"
* Create DATABASE_URL2: copy DATABASE_URL into it, but start it with start with "postgresql://" instead

Running on Heroku - updating Heroku code and database

* pg_dump -Fc -h localhost -U <yourdatabaseusername> amittsite > amittsite.dump  
* heroku pg:reset -a <your heroku app name>   
* heroku pg:push amittsite DATABASE_URL -a <your heroku app name> 
* git add .; git commit -m "heroku stuff"; git push heroku main