import os
import requests
from http.cookiejar import LWPCookieJar
from bs4 import BeautifulSoup

COOKIE_PATH = os.path.expanduser("~/.config/acchan/cookie.txt")

def get_session():
    """Create a session with loaded cookies (if any)"""
    session = requests.Session()
    jar = LWPCookieJar(COOKIE_PATH)
    try:
        jar.load(ignore_discard=True)
        session.cookies = jar
    except FileNotFoundError:
        pass
    return session

def is_logged_in(session: requests.Session) -> bool:
    """Check if the session is currently logged in to AtCoder."""
    res = session.get("https://atcoder.jp/home")
    soup = BeautifulSoup(res.text, "html.parser")
    return soup.find("a", href="/settings") is not None

