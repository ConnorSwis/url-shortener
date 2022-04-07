import base64
import os
import random
import sqlite3
from functools import wraps
import string


def seeded_uid(long_url, n: int):
    r = random.Random(long_url)
    s = (string.ascii_letters*3 + string.digits*2 + "!@#$%^*")
    uid = ''.join([r.choice(s) for _ in range(n)])
    return uid
    

class ShortUrls:
    def __init__(self):
        self.con = sqlite3.connect('./src/database/short_urls.db', check_same_thread=False)
        self.cur = self.con.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS short_urls (
            uid TEXT PRIMARY KEY,
            original_url TEXT NOT NULL
        )""")

    def _commit(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            self.con.commit()
            return result
        return wrapper

    def get_original_url(self, uid: str):
        """It does exactly what you think it does.

        Args:
            uid (str): The short id of the url.

        Returns:
            str: The original URL.
        """
        self.cur.execute(
            "SELECT * FROM short_urls WHERE uid=:uid",
            {'uid': uid}
        )
        original_url = self.cur.fetchone()
        if original_url:
            return original_url[1]

    @_commit
    def add_url(self, long_url: str, uid:str=None):
        uid = uid if uid else seeded_uid(long_url, 8)#generate_uid(8)
        try:
            self.cur.execute(
                "INSERT INTO short_urls(uid, original_url) VALUES (?, ?)",
                (
                    uid,
                    long_url
                )
            )
            return uid
        except sqlite3.IntegrityError:
            return False
            
    
    @_commit
    def remove_short_url(self, uid: str):
        self.cur.execute(
            "DELETE FROM short_urls WHERE uid=:uid",
            {'uid': uid}
        )
        
    def find_short_url(self, long_url):
        self.cur.execute(
            "SELECT * FROM short_urls WHERE original_url=:long_url",
            {'long_url': long_url}
        )
        return self.cur.fetchone()[0]
