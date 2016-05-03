import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('/opt/onadata/lib/python2.7/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append('/opt/onadata/src/onadata')

os.environ['DJANGO_SETTINGS_MODULE'] = 'onadata.settings.default_settings'

# Activate your virtual env
activate_env=os.path.expanduser("/opt/onadata/bin/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler() 
