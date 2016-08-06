# SUT CE Guild of Students Website

Requirements
============
* python 3
* pip
* virtual environemnt package
* Postgresql 9+


Before running
===============
Create a virtual environment (optional)

    virtualenv -p python3 venv
    source venv/bin/activate
    
Install dependencies:

    pip install -r requiremets.txt

Migrate and create database for first run:

    python manage.py migrate

Create a super usr to be able to log into admin:

    python manage.py createsuperuser

How to run
==========
Run lola run:

    python manage.py runserver 0.0.0.0:80


open [http://localhost/](http://127.0.0.1/) in your browser.

