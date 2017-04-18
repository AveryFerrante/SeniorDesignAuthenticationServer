import MySQLdb, string, random, hashlib
from cgi import parse_qs, escape

def generateSalt(size=20, chars=string.ascii_letters + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def getPostParams(environ):
	try:
		request_body_size = int(environ['CONTENT_LENGTH'])
		request_body = str(environ['wsgi.input'].read(request_body_size))
	except:
		request_body = "0"

	return parse_qs(request_body)

def application(environ, start_response):

	# Get the session object from the environ
	parameters = getPostParams(environ)

	try:
		username = escape(parameters['username'][0])
		password = escape(parameters['password'][0])
		pin = escape(parameters['pin'][0])
		userPassphrase = escape(parameters['passphrase'][0])
	except:
		start_response('200 OK', [('Content-type', 'text/plain')])
		return "ArgumentsError"

	salt = generateSalt()

	hasher = hashlib.sha512()
	hasher.update(password+salt)
	hashedword = hasher.hexdigest()

	db_pass_file = open('/var/www/default.conf')
	db_pass = db_pass_file.readlines()
	db = MySQLdb.connect(host = "localhost", user = "server", passwd = str(db_pass[0].rstrip()), db = "AuthenticationServer")
	cur = db.cursor()

	try:
		pin = int(pin)
	except:
		start_response('200 OK', [('Content-type', 'text/plain')])
		return "NonNumericalPin"

	try:
		cur.execute("INSERT INTO Users(user_name, password, pass_salt, secure_phrase, pin_number) VALUES(%s, %s, %s, %s, %s);", (username, hashedword, salt, userPassphrase, pin))
		db.commit()
		response = "Success"
	except:
		db.rollback()
		response = "UsernameError"

	db.close()

	start_response('200 OK', [('Content-type', 'text/plain')])
	return [response]
