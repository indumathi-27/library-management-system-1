from functools import wraps
from flask import g, request, redirect, session

class Actor:
    sess_key = ""
    route_url = "/"

    def uid(self):
        if self.isLoggedIn():
            return session[self.sess_key]
        return "err"

    def set_session(self, g):
        g.user = 0
        if self.isLoggedIn():
            g.user = session[self.sess_key]

    def isLoggedIn(self):
        return self.sess_key in session and session[self.sess_key] and session[self.sess_key] > 0

    def login_required(self, f, path="signin"):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if self.sess_key not in session or session[self.sess_key] is None:
                print(path)
                return redirect(self.route_url + path)
            return f(*args, **kwargs)
        return decorated_function

    def redirect_if_login(self, f, path="/"):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if self.sess_key in session and session[self.sess_key] is not None:
                return redirect(self.route_url + path)
            return f(*args, **kwargs)
        return decorated_function

    def signout(self):
        session.pop(self.sess_key, None)

    def signin(self, user_id):
        session[self.sess_key] = user_id
