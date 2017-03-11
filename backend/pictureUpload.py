import cgi #import parse_qs, escape
from tempfile import TemporaryFile
import os


def getPostParams(environ):
	try:
		request_body_size = int(environ['CONTENT_LENGTH'])
		request_body = str(environ['wsgi.input'].read(request_body_size))
	except (TypeError, ValueError):
		request_body = "0"

	return parse_qs(request_body)

def read(environ):
    length = int(environ.get('CONTENT_LENGTH', 0))
    stream = environ['wsgi.input']
    body = TemporaryFile(mode='w+b')
    while length > 0:
        part = stream.read(min(length, 1024*200)) # 200KB buffer size
        if not part: break
        body.write(part)
        length -= len(part)
    body.seek(0)
    environ['wsgi.input'] = body
    return body


def application(environ, start_response):
    # use cgi module to read data
    body = read(environ)
    form = cgi.FieldStorage(fp=body, environ=environ, keep_blank_values=True)
    # rest of your code

    fileitem = form['file']

    # Test if the file was uploaded
    if fileitem.filename:
        # strip leading path from file name
        # to avoid directory traversal attacks
        fn = os.path.basename(fileitem.filename)
        open('/var/www/html/backend/' + fn, 'wb').write(fileitem.file.read())
        message = 'The file "' + fn + '" was uploaded successfully'
    else:
        returningResponse = "No file was uploaded"

	start_response('200 OK', [('Content-type', 'text/plain')])
	return returningResponse
