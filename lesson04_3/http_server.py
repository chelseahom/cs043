import wsgiref.simple_server

def application(environ, start_response):
    headers = [('Content-Type', 'text/plain; charset=utf-8')]
    start_response('200 OK', headers)
    return ['"Good morning, Sunshine!"'.encode()]

# opens a simple server in local host listening to port 8080
httpd = wsgiref.simple_server.make_server('', 8080, application)
httpd.serve_forever()
