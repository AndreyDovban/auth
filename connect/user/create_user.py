import sqlite3
from connect.create_tables.create_users import create_users
import bcrypt


def create_user(id, name, description, role, password):
    with sqlite3.connect('../base.db', check_same_thread=False) as con:
        cur = con.cursor()

        create_users(cur)

        cur.execute(
            f'''SELECT EXISTS 
                    (SELECT * FROM users 
                    WHERE name = "{name}")'''
        )
        target_user = cur.fetchone()[0]
        print(target_user)

        salt = bcrypt.gensalt()

        hashAndSalt = bcrypt.hashpw(password.encode(), salt)

        print(hashAndSalt)

        if target_user == 0:
            cur.execute(
                f'''INSERT INTO users (uuid, name, description, role, password)
                    VALUES ("{id}", "{name}", "{description}", "{role}",  "{hashAndSalt}")'''
            )

        # if target_user == 0:
        #     cur.execute("INSERT INTO users (uuid, name, description, role, password) VALUES (?, ?, ?, ?, ?)",
        #                 (id, name, description, role, hashAndSalt))

        if target_user == 1:
            return {"error": "403", "message": "User " + name + " is exists"}

        con.commit()
        cur.close()

        return {"message": "User added successfully"}
