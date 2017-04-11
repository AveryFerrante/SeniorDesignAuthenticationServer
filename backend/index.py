import string, random, MySQLdb


configuration_file = open('/var/www/default.conf')
configuration_data = configuration_file.readlines()

def generateRandomString(size=20, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def createEntry(stringId):
    db = MySQLdb.connect(host = "localhost", user = "server", passwd = str(configuration_data[0].rstrip()), db = "AuthenticationServer")
    cur = db.cursor()

    cur.execute("INSERT INTO ActiveCodes(session_id, expire_time) VALUES (%s, NOW() + INTERVAL 5 MINUTE)",  (stringId,))
    db.commit() # Commit the insert to the database
    db.close()

def application(environ, start_response):
    stringId = generateRandomString()
    createEntry(stringId)
    returnHtml = """
    <!DOCTYPE html>
    <html>

      <head>
        <title>Auth Server</title>
        <style>
            img.center {
              margin: auto;
              position: absolute;
              top: 0; left: 0; bottom: 0; right: 0;
            }
            body {
              background-color: #d3d3d3;
            }
        </style>
      </head>

      <body>

        <a href="../signup.html">
          <img class="center" src='https://api.qrserver.com/v1/create-qr-code/?size=300x300&data="""+stringId+"""' alt='QR Code'>
        </a>

      </body>
    </html>
    """
    start_response('200 OK', [('Content-type', 'text/html')])
    return returnHtml
