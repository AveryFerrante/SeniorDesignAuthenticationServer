import MySQLdb, hashlib, string, random, datetime
from beaker.middleware import SessionMiddleware
from cgi import parse_qs, escape


def generateString(size=20, chars=string.ascii_letters + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

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
	cur.execute("SELECT user_id FROM Users WHERE user_name=%s AND password=%s", (username, hasher.hexdigest()))
	for row in cur.fetchall():
		if not row:
			db.close()
			return False
		else:
			user_id = row[0]
			db.close()
			return user_id

def getTimeoutTime():
	future_time = datetime.datetime.now() + datetime.timedelta(seconds = int(configuration_data[2].rstrip()))
	return future_time.strftime('%Y-%m-%d %H:%M:%S')

def createSession(user_id):
	db = MySQLdb.connect(host = "localhost", user = "server", passwd = str(configuration_data[0].rstrip()), db = "AuthenticationServer")
	cur = db.cursor()

	session_string = generateString()
	active_state = 1
	date_string = getTimeoutTime()
	cur.execute("INSERT INTO Sessions(user_id, session_id, active, expire_time) VALUES (%s, %s, %s, %s)", (int(user_id), session_string, active_state, date_string))
	db.commit() # Commit the insert to the database
	db.close()
	return session_string




def simple_app(environ, start_response):
	# Get the session object from the environ
	session = environ['beaker.session']



	if 'logged_in' in session and session['logged_in'] is True:
		returningResponse = "Granted"
	else:
		# Get the arguments passed from the API call
		try:
			parameters = getPostParams(environ)
			username = str(escape(parameters['username'][0]))
			password = str(escape(parameters['password'][0]))
		except:
			returningResponse = "MissingArgument"


		user_id = checkUsernamePassword(username, password)
		if user_id:
			# Insert session section into database
			session_string = createSession(user_id)
			session['logged_in'] = True
			session['session_string'] = session_string
			returningResponse = "Granted"
		else:
			session['logged_in'] = False
			returningResponse = "NotFound"

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
