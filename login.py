import os
from http.cookiejar import LWPCookieJar, Cookie
from utils.session_helper import is_logged_in, get_session

def login():
    # Setup cookie path
    cookie_path = os.path.expanduser("~/.config/acchan/cookie.txt")
    os.makedirs(os.path.dirname(cookie_path), exist_ok=True)

    # Ask user for REVEL_SESSION value
    revel_value = input("Paste your REVEL_SESSION cookie: ").strip()

    # Build a Cookie object manually
    cookie = Cookie(
        version=0,
        name="REVEL_SESSION",
        value=revel_value,
        port=None,
        port_specified=False,
        domain=".atcoder.jp",
        domain_specified=True,
        domain_initial_dot=True,
        path="/",
        path_specified=True,
        secure=False,
        expires=None,
        discard=True,
        comment=None,
        comment_url=None,
        rest={},
        rfc2109=False
    )

    # Save cookie to file
    jar = LWPCookieJar(cookie_path)
    jar.set_cookie(cookie)
    jar.save(ignore_discard=True)
    print("✅ Cookie saved.")

    # Confirm login
    session = get_session()
    if is_logged_in(session):
        print("✅ Logged in successfully.")
    else:
        print("❌ Login failed.")

