from __future__ import unicode_literals
import multiprocessing

bind = "unix:/home/shora/website-django/gunicorn.sock"
workers = 4
errorlog = "/home/shora/logs/shora_gunicorn.log"
loglevel = "debug"
proc_name = "shora"

