# Used Finance from CS50 to help write this file
import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    # Render an apology message to users
    def escape(s):
     #   for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
      #                   ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
       #     s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            ## Might have to change /login to whatever my login page is called
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"