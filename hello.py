#!/usr/bin/env python3
import cgi, os
import secret
import json
from cgi import escape
from datetime import date

def cgi_script():

    # ===== Show the users environment variables in json ====
    # environment_json()

    # ==== Show users browser in HTML ====
    # show_browser()
    # ==== Login Form =====
    if os.environ.get("REQUEST_METHOD") == "POST":
        data = cgi.FieldStorage()
        username = data['username'].value
        password = data['password'].value
        if is_correct_uandp(username, password):
            display_with_cook(username, password)
        else:
            display_post_data(username, password)
    else:
        # environment_json()
        login_page()
        if os.environ.get("HTTP_COOKIE"):
            username = None
            password = None
            cookies = os.environ['HTTP_COOKIE']
            cookies = cookies.split('; ')
            for cookie in cookies:
                cookie = cookie.split('=')
                username = cookie[0]
                password = cookie[1]
            print(secret_page(username, password))

# Secret Page
def secret_page(username=None, password=None):
    """
    Returns the HTML for the page visited after the user has logged-in.
    """
    if username is None or password is None:
        raise ValueError("You need to pass both username and password!")

    return _wrapper("""
    <h1> Welcome, {username}! </h1>

    <p> <small> Pst! I know your password is
        <span class="spoilers"> {password}</span>.
        </small>
    </p>
    """.format(username=escape(username.capitalize()),
               password=escape(password)))

    # ==== Edit username and pw ion secret.py ====
def is_correct_uandp(username, password):
    if username == secret.username and password == secret.password:
        return True
    return False

def display_with_cook(u, p):
    print("Set-Cookie: {u} = {p};".format(u=u, p=p))
    print("Content-Type:text/html\r\n\r\n")
    print(_wrapper(r"""
            <h1>POSTED</h1>
            <h3>Username: {uname}</h3>
            <h3>Password: {pw}</h3>
        """.format(uname=u, pw=p)))

def display_post_data(username, password):
    print("Content-Type:text/html\r\n\r\n")
    print(_wrapper(r"""
        <h1>POSTED</h1>
        <h3>Username: {uname}</h3>
        <h3>Password: {pw}</h3>
    """.format(uname=username, pw=password)))

def environment_json():
    print("Content-type:application/json\n")
    env_json = json.dumps(
        {k: os.environ.get(k) for k, v in os.environ.items()}
    )
    print(env_json)

def show_browser():
    print("Content-Type:text/html\n")
    print("<html><body><h1>Browser: {browser} </h1></body></html>".format(browser=os.environ.get("HTTP_USER_AGENT")))

def login_page():
    """
    Returns the HTML for the login page.
    """
    print("Content-Type:text/html\n")
    print(_wrapper(r"""
    <h1> Welcome! </h1>

    <form method="POST" action="hello.py">
        <label> <span>Username:</span> <input autofocus type="text" name="username"></label> <br>
        <label> <span>Password:</span> <input type="password" name="password"></label>

        <button type="submit"> Login! </button>
    </form>
    """))

def _wrapper(page):
    """
    Wraps some text in common HTML.
    """
    return ("""
    <!DOCTYPE HTML>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, sans-serif;
                max-width: 24em;
                margin: auto;
                color: #333;
                background-color: #fdfdfd
            }

            .spoilers {
                color: rgba(0,0,0,0); border-bottom: 1px dashed #ccc
            }
            .spoilers:hover {
                transition: color 250ms;
                color: rgba(36, 36, 36, 1)
            }

            label {
                display: flex;
                flex-direction: row;
            }

            label > span {
                flex: 0;
            }

            label> input {
                flex: 1;
            }

            button {
                font-size: larger;
                float: right;
                margin-top: 6px;
            }
        </style>
    </head>
    <body>
    """ + page + """
    </body>
    </html>
    """)

if __name__ == "__main__":
    cgi_script()