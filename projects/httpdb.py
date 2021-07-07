import wsgiref.simple_server
import urllib.parse
from database import Simpledb

def application(environ, start_response):
    headers = [('Content-Type', 'text/plain; charset=utf-8')]

    path = environ['PATH_INFO']
    params = urllib.parse.parse_qs(environ['QUERY_STRING'])
    # opens a text file
    db = Simpledb('db.txt')
    # check if the name is already in the text file
    s = db.select_one(params['key'][0])

    if path == '/insert':
        # inserts inputed number into the database
        # if the name is already there, replace with new number
        db.insert(params['key'][0], params['value'][0])
        start_response('200 OK', headers)
        return ['Inserted'.encode()]

    elif path == '/select':
        # checks if the given name is in the database
        # if it found, return the number; otherwise return NULL
        start_response('200 OK', headers)
        if s:
            return [s.encode()]
        else:
            return ['NULL'.encode()]

    elif path == '/delete':
        # checks if the given name is in the database
        # if it found, delete the number; otherwise return NULL
        start_response('200 OK', headers)
        if s:
            db.delete(params['key'][0])
            return['Deleted'.encode()]
        else:
            return['NULL'.encode()]

    elif path == '/update':
        # checks if the given name is in the database
        # if it found, update the number; otherwise return NULL
        start_response('200 OK', headers)
        if s:
            db.update(params['key'][0], params['value'][0])
            return ['Updated'.encode()]
        else:
            return ['NULL'.encode()]
    else:
        start_response('404 Not Found', headers)
        return ['Status 404: Resource not found'.encode()]

# opens a simple server in the local host listening to port 8081
httpd = wsgiref.simple_server.make_server('', 8081, application)
httpd.serve_forever()
