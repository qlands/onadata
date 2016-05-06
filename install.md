# Installation instructions
## Prepare the Os
### Ubuntu required packages  
    sudo apt-get update
    sudo apt-get install  postgresql-9.3-postgis-2.1 binutils libproj-dev gdal-bin memcached libmemcached-dev build-essential python-pip python-virtualenv python-dev git libssl-dev libpq-dev gfortran libatlas-base-dev libjpeg-dev libxml2-dev libxslt-dev zlib1g-dev python-software-properties ghostscript python-celery python-sphinx openjdk-7-jdk openjdk-7-jre  postgresql-9.3-postgis-2.1-scripts rabbitmq-server librabbitmq-dev mongodb

## Database setup
Replace username and db name accordingly. Later on you will need to indicate this parameters in the configuration file.

    sudo su postgres -c "psql -c \"CREATE USER onadata WITH PASSWORD 'onadata';\""
    sudo su postgres -c "psql -c \"CREATE DATABASE onadata OWNER onadata;\""
    sudo su postgres -c "psql -d onadata -c \"CREATE EXTENSION IF NOT EXISTS postgis;\""
    sudo su postgres -c "psql -d onadata -c \"CREATE EXTENSION IF NOT EXISTS postgis_topology;\""

## Create python virtual environment and activate it
Note: This instructions assume that OnaData will be installed in /opt and the user installing it is not root. The non-root-user will own the onadata directory.

    cd /opt
    sudo virtualenv onadata
    sudo chown -R non-root-user onadata
    source /opt/onadata/bin/activate
    mkdir /opt/onadata/src

## Get the code
    cd /opt/onadata/src
    git clone https://github.com/qlands/onadata.git
    cd /opt/onadata/src/onadata/

## Install required python packages
    pip install -r requirements/base.pip --allow-all-external
    pip install numpy pandas==0.12.0
    python requirements/django-nose/setup.py install

## Edit the configuration scripts
### Edit /opt/onadata/src/onadata/onadata/settings/default_settings.py
Find the section below and edit NAME,USER,PASSWORD with the setting you used in the database setup. If you used a different host edit HOST

     DATABASES = {
    'default': {
    'ENGINE': 'django.contrib.gis.db.backends.postgis',
    'NAME': 'onadata',
    'USER': 'onadata',
    'PASSWORD': '',
    'HOST': '127.0.0.1',
    'OPTIONS': {
        # note: this option obsolete starting with django 1.6
        'autocommit': True,
    }}}

### Edit /opt/onadata/src/onadata/onadata/settings/common.py
Find the section below and edit HOST, PORST, NAME, USER and PASSWORD if necessary. The Installation of Mongo does not set an user or password for the database.  

    MONGO_DATABASE = {
    'HOST': 'localhost',
    'PORT': 27017,
    'NAME': 'formhub',
    'USER': '',
    'PASSWORD': ''
    }

## Test the Installation

    cd /opt/onadata/src/onadata/
    export PYTHONPATH=$PYTHONPATH:/opt/onadata/src/onadata
    export DJANGO_SETTINGS_MODULE=onadata.settings.default_settings
    python manage.py validate

The validate should return 0 errors.

## Initial db setup
    python manage.py syncdb --noinput
    python manage.py migrate

## Setup celery service

Celery is used by OnaData to run time-consuming processes like the data exports as distributed tasks.
### Edit the /opt/onadata/src/onadata/extras/celeryd/etc/default/celeryd file

Change the following lines to look like the below:

      CELERYD_CHDIR="/opt/onadata/src/onadata/"
      ENV_PYTHON="/opt/onadata/bin/python"
      CELERYD_USER="www-data"
      CELERYD_GROUP="www-data"
      export DJANGO_SETTINGS_MODULE="onadata.settings.default_settings"

### Set the celeryd as a service

Create a symbolic link to the celery file from de init.d directory. Note /etc/default must exists.

      sudo ln -s /opt/onadata/src/onadata/extras/celeryd/etc/default/celeryd /etc/default/celeryd
      sudo ln -s /opt/onadata/src/onadata/extras/celeryd/etc/init.d/celeryd /etc/init.d/celeryd
      sudo /etc/init.d/celeryd start

The startup of celery should return something like the below:

      celery multi v3.1.15 (Cipater)
      > Starting nodes...
      Your environment is:"onadata.settings.default_settings"
      > w1@SlackOna: OK

## Create a super user
      python manage.py createsuperuser

## Copy all files from your static folders into the STATIC_ROOT directory
      python manage.py collectstatic --noinput

## Run OnaData for testing

    cd /opt/onadata/src/onadata
    python manage.py runserver

Running the server should return something like the below:

      Your environment is:"onadata.settings.default_settings"
      Your environment is:"onadata.settings.default_settings"
      Validating models...
      0 errors found
      April 21, 2016 - 08:26:37
      Django version 1.6.11, using settings 'onadata.settings.default_settings'
      Starting development server at http://127.0.0.1:8000/
      Quit the server with CONTROL-C.

Using the Internet browser go to http://127.0.0.1:8000/  You will see the OnaData front page. Test the long in page with the super user.

## compile api docs
    cd docs
    make html
    cd ..

## Make Apache web server to load OnaData
### Install required packages

    sudo apt-get install apache2 libapache2-mod-wsgi

### Copy the apache configuration files to the apache conf directory

    sudo cp /opt/onadata/src/onadata/extras/wsgi/apache-onadata.conf /etc/apache2/sites-available
    cd /etc/apache2/sites-enabled
    sudo ln -s ../sites-available/apache-onadata.conf ./apache-onadata.conf

Go to http://localhost OnaData should be running from there.
