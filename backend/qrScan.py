from beaker.middleware import SessionMiddleware
from cgi import parse_qs, escape
import datetime


def simple_app(environ, start_response):
	# Get the session object from the environ
	session = environ['beaker.session']


	if 'logged_in' in session and session['logged_in'] is True:
		# Get Session_id and check against the database (can get the user_id associated to get the image # to return to the user)
		returningResponse = "Granted"
	else:
        returningResponse = "NoSessionCookie"

	session.save()
	start_response('200 OK', [('Content-type', 'text/plain')])
	return returningResponse


# Configure the SessionMiddleware
configuration_file = open('/var/www/default.conf')
configuration_data = configuration_file.readlines()
session_opts = {
    'session.type': 'cookie', # All data is stored in a cookie on the client side (cannot exceed 4096 bytes)
    'auto': True,
    'session.cookie_expires': int(configuration_data[2].rstrip()),
    'session.validate_key': str(configuration_data[1].rstrip())
}
application = SessionMiddleware(simple_app, session_opts)
