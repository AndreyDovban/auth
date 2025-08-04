from flask import Flask, request, render_template
import uuid
import os
from connect.user.create_user import create_user
from connect.user.get_users import get_users
from connect.user.delete_user import delete_users


app = Flask(__name__, static_url_path='/static')


@app.route("/")
def index():
    return '<h1> Home </h1>'


@app.route("/user")
def user():
    return render_template('user.html')


@app.route("/api/user",  methods=["GET", "POST", "DELETE"])
# Работа с сущностью продукт
def product():
    os.system("clear")

    print("work api product ", request.method)

    if request.method == "GET":
        print("work")
        return get_users()

    if request.method == "POST":
        user = request.form
        user_id = uuid.uuid4().hex
        return create_user(user_id, user["name"], user["description"], user["role"], user["password"])

    if request.method == "DELETE":
        user = request.get_json()
        return delete_users(user["id"])


if __name__ == "__main__":
    app.run(debug=True)
