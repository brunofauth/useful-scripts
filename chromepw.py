#! /usr/bin/env python


import sqlite3
import sys
import os


CMD = "SELECT action_url, username_value, password_value FROM logins"
PATHS = {
    "win32": (lambda: os.environ["LOCALAPPDATA"] + r"\Google\Chrome\User Data\Default\Login Data"),
    "darwin": (lambda: os.path.expandvars(r"~/Library/Application Support/Google/Chrome/Default/Login Data")),
    "linux": (lambda: os.path.expanduser(r"~/.config/chromium/Default/Login Data"))
}


def iter_data():
    if sys.platform == "win32":
        import win32crypt
        pw_func = lambda x: win32crypt.CryptUnprotectData(x)[1]
    else:
        pw_func = lambda x: x
    connection = sqlite3.connect(PATHS[sys.platform]())
    for url, user, pw in connection.execute(CMD).fetchall():
        if user:
            yield url, user, pw_func(pw)


def main():
    print("Website, Username, Password:", file=sys.stderr)
    print("\n".join(f'"{w}", "{u}", "{p}"' for w, u, p in iter_data()))


if __name__ == "__main__":
    main()


