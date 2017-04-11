import MySQLdb
from beaker.middleware import SessionMiddleware
from cgi import parse_qs, escape


def getPostParams(environ):
	try:
		request_body_size = int(environ['CONTENT_LENGTH'])
		request_body = str(environ['wsgi.input'].read(request_body_size))
	except (TypeError, ValueError):
		request_body = "0"

	return parse_qs(request_body)

def getUserPhrase(session_id):
	try:
		db = MySQLdb.connect(host = "localhost", user = "server", passwd = str(configuration_data[0].rstrip()), db = "AuthenticationServer")
		cur = db.cursor()

		cur.execute("SELECT * FROM Sessions WHERE session_id = %s", (session_id,))
		result = cur.fetchone()
		user_id = result[1]

		cur.execute("SELECT secure_phrase FROM Users WHERE user_id = %s", (user_id,))
		phrase = cur.fetchone()[0]

		return phrase
	except:
		return "<strong>FUCKED UP!</strong>"

def setActiveCode(code):
	try:
		db = MySQLdb.connect(host = "localhost", user = "server", passwd = str(configuration_data[0].rstrip()), db = "AuthenticationServer")
		cur = db.cursor()

		cur.execute("UPDATE ActiveCodes SET active = 1 WHERE session_id = %s", (code,))
		db.commit()
		db.close()
		return 1
	except:
		return 0



def simple_app(environ, start_response):
	# Get the session object from the environ
	session = environ['beaker.session']


	if 'logged_in' in session and session['logged_in'] is True:
		# Get Session_id and check against the database (can get the user_id associated to get the image # to return to the user)
		try:
			parameters = getPostParams(environ)
			code = str(escape(parameters['qrCode'][0]))
			if setActiveCode(code) is 1:
				returningResponse = getUserPhrase(session['session_string'])
			else:
				returningResponse = "InvalidScannedCode"
		except:
			returningResponse = "NoScannedCode"
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
