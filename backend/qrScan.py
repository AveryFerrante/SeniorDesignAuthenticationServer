from beaker.middleware import SessionMiddleware
from cgi import parse_qs, escape



def simple_app(environ, start_response):
	# Get the session object from the environ
	session = environ['beaker.session']


	if 'logged_in' in session and session['logged_in'] is True:
		returningResponse = "Granted"
	else:
        returningResponse = "NoSessionCookie"

	session.save()
	start_response('200 OK', [('Content-type', 'text/plain')])
	return returningResponse


# Configure the SessionMiddleware
validate_key_file = open('/var/www/default.conf')
validate_key = validate_key_file.readlines()
session_opts = {
    'session.type': 'cookie', # All data is stored in a cookie on the client side (cannot exceed 4096 bytes)
    'auto': True,
    'session.cookie_expires': 60,
    'session.validate_key': str(validate_key[1].rstrip())
}
application = SessionMiddleware(simple_app, session_opts)
