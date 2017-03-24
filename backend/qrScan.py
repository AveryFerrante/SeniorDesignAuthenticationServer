import MySQLdb
from beaker.middleware import SessionMiddleware

def getImageNumber(session_id):
	try:
		db = MySQLdb.connect(host = "localhost", user = "server", passwd = str(configuration_data[0].rstrip()), db = "AuthenticationServer")
		cur = db.cursor()

		cur.execute("SELECT * FROM Sessions WHERE session_id = %s", (session_id,))
		result = cur.fetchone()
		user_id = result[1]

		cur.execute("SELECT image_number FROM Users WHERE user_id = %s", (user_id,))
		image_number = cur.fetchone()[0]

		return "images/" + str(image_number) + ".jpg"
	except:
		return "<strong>FUCKED UP!</strong>"

def simple_app(environ, start_response):
	# Get the session object from the environ
	session = environ['beaker.session']


	if 'logged_in' in session and session['logged_in'] is True:
		# Get Session_id and check against the database (can get the user_id associated to get the image # to return to the user)
		returningResponse = getImageNumber(session['session_string'])
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
