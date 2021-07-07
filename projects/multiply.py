import sqlite3
import wsgiref.simple_server
import urllib.parse
import http.cookies
import random

connection = sqlite3.connect('users.db')
stmt = "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
cursor = connection.cursor()
result = cursor.execute(stmt)
r = result.fetchall()
if r == []:
    exp = 'CREATE TABLE users (username,password)'
    connection.execute(exp)


def application(environ, start_response):
    headers = [('Content-Type', 'text/html; charset=utf-8')]

    path = environ['PATH_INFO']
    params = urllib.parse.parse_qs(environ['QUERY_STRING'])
    un = params['username'][0] if 'username' in params else None
    pw = params['password'][0] if 'password' in params else None

    import pdb
    pdb.set_trace()
    if path == '/register' and un and pw:
        user = cursor.execute('SELECT * FROM users WHERE username = ?', [un]).fetchall()
        if user:
            start_response('200 OK', headers)
            return ['Sorry, username {} is taken'.format(un).encode()]
        else:
            connection.execute('INSERT INTO users VALUES (?, ?)', [un, pw])
            connection.commit()
            return ['Your username and password have been successfully registered.']

    elif path == '/login' and un and pw:
        user = cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', [un, pw]).fetchall()
        if user:
            headers.append(('Set-Cookie', 'session={}:{}'.format(un, pw)))
            start_response('200 OK', headers)
            return ['User {} successfully logged in. <a href="/account">Account</a>'.format(un).encode()]
        else:
            start_response('200 OK', headers)
            return ['Incorrect username or password'.encode()]

    elif path == '/logout':
        headers.append(('Set-Cookie', 'session=0; expires=Thu, 01 Jan 1970 00:00:00 GMT'))
        start_response('200 OK', headers)
        return ['Logged out. <a href="/">Login</a>'.encode()]

    elif path == '/account':
        start_response('200 OK', headers)

        if 'HTTP_COOKIE' not in environ:
            return ['Not logged in <a href="/">Login</a>'.encode()]

        cookies = http.cookies.SimpleCookie()
        cookies.load(environ['HTTP_COOKIE'])
        if 'session' not in cookies:
            return ['Not logged in <a href="/">Login</a>'.encode()]

        [un, pw] = cookies['session'].value.split(':')
        user = cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', [un, pw]).fetchall()

        #This is where the game begins. This section of is code only executed if the login form works, and if the user is successfully logged in
        if user:
            correct = 0
            wrong = 0

            cookies = http.cookies.SimpleCookie()
            if 'HTTP_COOKIE' in environ:
                cookies.load(environ['HTTP_COOKIE'])
                if 'score' in cookies:
                    [correct, wrong] = cookies['score'].value.split(':')

            page = '<!DOCTYPE html><html><head><title>Multiply with Score</title></head><body>'
            if 'factor1' in params and 'factor2' in params and 'answer' in params:
                f1 = int(params['factor1'][0])
                f2 = int(params['factor2'][0])
                answer = int(params['answer'][0])
                if answer == f1 * f2:
                    correct += 1
                    page = page + '<h1>Your answer is correct.</h1>'
                else:
                    wrong += 1
                    page = page + '<h1>Your answer is wrong.</h1>'

            elif 'reset' in params:
                correct = 0
                wrong = 0

            headers.append(('Set-Cookie', 'score={}:{}'.format(correct, wrong)))

            f1 = random.randrange(10) + 1
            f2 = random.randrange(10) + 1

            page = page + '<h1>What is {} x {}</h1>'.format(f1, f2)

            answer = [f1*f2, f1+f2, f1-f2, f2-f1]
            random.shuffle(answer)

            hyperlink1 = '<a href="/account?username={}&amp;password={}&amp;factor1={}&amp;factor2={}&amp;answer={}">{}: {}</a><br>'.format(un, pw, f1, f2, answer[0], 'A', str(answer[0]))
            hyperlink2 = '<a href="/account?username={}&amp;password={}&amp;factor1={}&amp;factor2={}&amp;answer={}">{}: {}</a><br>'.format(un, pw, f1, f2, answer[1], 'B', str(answer[1]))
            hyperlink3 = '<a href="/account?username={}&amp;password={}&amp;factor1={}&amp;factor2={}&amp;answer={}">{}: {}</a><br>'.format(un, pw, f1, f2, answer[2], 'C', str(answer[2]))
            hyperlink4 = '<a href="/account?username={}&amp;password={}&amp;factor1={}&amp;factor2={}&amp;answer={}">{}: {}</a><br>'.format(un, pw, f1, f2, answer[3], 'D', str(answer[3]))
            page = page + hyperlink1 + hyperlink2 + hyperlink3 + hyperlink4

            page += '''<h2>Score</h2>
            Correct: {}<br>
            Wrong: {}<br>
            <a href="/account?reset=true">Reset</a>
            </body></html>'''.format(correct, wrong)

            return [page.encode()]
        else:
            return ['Not logged in. <a href="/">Login</a>'.encode()]

    elif path == '/':
        start_response('200 OK', headers)
        page = '''<!DOCTYPE html>
        <html>
        <head><title>Multiplication Form</title></head>
        <body>
        <h1>Login Form</h1>
        <form action = "/login" style = "background-color:gold">
            <h1> Login </h1>
            Username <input type = "text" name = "username"> <br>
            Password <input type = "password" name = "password"> <br>
            <input type = "submit" value = "Log in">
        </form>
        <form action = "/register" style = "background-color:gold">
            <h1> Register </h1>
            Username <input type = "text" name = "username"> <br>
            Password <input type = "password" name = "password"> <br>
            <input type = "submit" value = "Register">
        </form> 
        <hr>
        </body> </html>'''

        return [page.encode()]

    else:
        start_response('404 Not Found', headers)
        return ['Status 404: Resource not found'.encode()]


httpd = wsgiref.simple_server.make_server('', 8000, application)
httpd.serve_forever()