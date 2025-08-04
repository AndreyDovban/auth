import sqlite3
from connect.create_tables.create_users import create_users
import bcrypt


def login(name, password):
    with sqlite3.connect('../base.db', check_same_thread=False) as con:
        cur = con.cursor()

        create_users(cur)

        cur.execute(
            f'''SELECT * FROM  users 
                WHERE name = "{name}"
                '''
        )
        user = cur.fetchone()

        if user is None:
            cur.close()
            return {"error": "401", "message": "Login or password is incorrect"}

        if bcrypt.checkpw(password.encode(), user[4].encode()):
            cur.close()
            return list(user)
        else:
            print("Пароль не совпадает")
            cur.close()
            return {"error": "401", "message": "Login or password is incorrect"}
