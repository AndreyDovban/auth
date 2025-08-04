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

        print("HASH", user[1],  user[4])

        if user[0] is None:
            return {"error": "401", "message": "Login or password is incorrect"}

        if bcrypt.checkpw(password.encode(), user[4][2:-1].encode()):
            return user[0]
        else:
            print("Пароль не совпадает")
            return {"error": "401", "message": "Login or password is incorrect"}

        cur.close()

        return user
