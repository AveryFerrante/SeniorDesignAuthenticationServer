import MySQLdb
from cgi import parse_qs, escape

def getPostParams(environ):
    request_body_size = int(environ['CONTENT_LENGTH'])
    request_body = str(environ['wsgi.input'].read(request_body_size))
    return parse_qs(request_body)



def application(environ, start_response):

    parameters = getPostParams(environ)
    code = parameters['code'][0]
    try:
        money = parameters['money'][0]

        db_pass_file = open('/var/www/default.conf')
        db_pass = db_pass_file.readlines()
        db = MySQLdb.connect(host = "localhost", user = "server", passwd = str(db_pass[0].rstrip()), db = "AuthenticationServer")
        cur = db.cursor()

        cur.execute("UPDATE ActiveCodes SET money_amount = %s WHERE session_id = %s", (money, code))
        db.commit()

        response = "Added"
        start_response('200 OK', [('Content-type', 'text/plain')])
        return [response]

    except:

        db_pass_file = open('/var/www/default.conf')
        db_pass = db_pass_file.readlines()
        db = MySQLdb.connect(host = "localhost", user = "server", passwd = str(db_pass[0].rstrip()), db = "AuthenticationServer")
        cur = db.cursor()

        cur.execute("SELECT money_amount FROM ActiveCodes WHERE session_id = %s AND active IS NOT NULL AND money_amount IS NOT NULL", (code, ))
        record = cur.fetchone()
        response = str(record[0])

        start_response('200 OK', [('Content-type', 'text/plain')])
        return [response]
