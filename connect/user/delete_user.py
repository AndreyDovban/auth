import sqlite3
from connect.create_tables.create_users import create_users


def delete_users(id):
    with sqlite3.connect('../base.db', check_same_thread=False) as con:
        cur = con.cursor()

        cur.execute(
            f'''DELETE FROM  users
                WHERE uuid = "{id}"
                '''
        )

        con.commit()
        cur.close()

        return {"message": "User deleted successfully"}
