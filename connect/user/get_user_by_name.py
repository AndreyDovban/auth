import sqlite3
from connect.create_tables.create_users import create_users


def get_user_by_name(name):
    with sqlite3.connect('../users-base.db', check_same_thread=False) as con:
        cur = con.cursor()

        create_users(cur)

        cur.execute(
            f'''SELECT * FROM  users
                WHERE name = "{name}"
                '''
        )
        data = cur.fetchone()

        cur.close()

        return {"code": "200", "data":  data}
