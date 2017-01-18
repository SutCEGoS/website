#!/bin/sh

log_file_name="deploy_$(date +%Y-%m-%d.%H:%M:%S).log"
log_directory="/home/shora/logs/deploy/"
log_file="$log_directory$log_file_name"

mkdir -p $log_directory
touch $log_file

exec &> >(tee -a "$log_file")

echo Deploy started
echo User: $USER

echo Activating virtual environment
. ~/venv/bin/activate

echo Installing new python dependencies
pip install -U -r requirements.txt

echo Collecting static files
python manage.py collectstatic --noinput -c -l

echo Migrating database
python manage.py migrate

echo Reload uwsgi
pkill uwsgi

sudo nginx reload

echo Deployment finished. Check logs in $log_file
