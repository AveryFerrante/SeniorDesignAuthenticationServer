import MySQLdb, hashlib
from beaker.middleware import SessionMiddleware
from cgi import parse_qs, escape




def getPostParams(environ):
	try:
		request_body_size = int(environ['CONTENT_LENGTH'])
		request_body = str(environ['wsgi.input'].read(request_body_size))
	except (TypeError, ValueError):
		request_body = "0"

	return parse_qs(request_body)

def checkUsernamePassword(username, password):
	db_pass_file = open('/var/www/default.conf')
	db_pass = db_pass_file.readlines()
	db = MySQLdb.connect(host = "localhost", user = "server", passwd = str(db_pass[0].rstrip()), db = "AuthenticationServer")
	cur = db.cursor()

	# Fetch associated password salt and append to entered password
	cur.execute("SELECT pass_salt FROM Users WHERE user_name=%s", (username,))
	for row in cur.fetchall():
		password += row[0]

	# Hash the password and the added salt
	hasher = hashlib.sha512()
	hasher.update(password)

	# Determine if the user entered correct credentials
	cur.execute("SELECT * FROM Users WHERE user_name=%s AND password=%s", (username, hasher.hexdigest()))
	if not cur.fetchone():
		db.close()
		return True
	else:
		db.close()
		return False



def simple_app(environ, start_response):
	# Get the session object from the environ
	session = environ['beaker.session']

	returningResponse = "DefaultResponse"

	if 'logged_in' in session and session['logged_in'] is True:
		returningResponse = "Granted"
	else:
		# Get the arguments passed from the API call
		try:
			parameters = getPostParams(environ)
			username = str(escape(parameters['username'][0]))
			password = str(escape(parameters['password'][0]))
		except:
			session.save()
			start_response('200 OK', [('Content-type', 'text/plain')])
			return "MissingArgument"


			if checkUsernamePassword(username, password):
				returningResponse = "Granted"
				session['logged_in'] = True
			else:
				returningResponse = "NotFound"
				session['logged_in'] = False


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
