from flask import Flask, request, render_template
import uuid
import os
from connect.user.create_user import create_user
from connect.user.get_users import get_users
from connect.user.delete_user import delete_users
from connect.login.login import login


app = Flask(__name__, static_url_path='/static')


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/api/user",  methods=["GET", "POST", "DELETE"])
# Работа с сущностью продукт
def user():
    print("work api user ", request.method)

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


@app.route("/api/login",  methods=["POST"])
# Работа с сущностью продукт
def login_handler():
    os.system("clear")

    print("work api login ", request.method)

    if request.method == "POST":
        user = request.form
        return login(user["name"], user["password"])


if __name__ == "__main__":
    app.run(debug=True)
