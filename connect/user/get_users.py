import sqlite3
from connect.create_tables.create_users import create_users


def get_users():
    with sqlite3.connect('../users-base.db', check_same_thread=False) as con:
        cur = con.cursor()

        create_users(cur)

        cur.execute(
            f'''SELECT * FROM  users
                '''
        )
        data = cur.fetchall()

        cur.close()

        return data
