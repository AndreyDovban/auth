from flask import Flask, request, render_template, jsonify, make_response
import uuid
from connect.user.create_user import create_user
from connect.user.get_users import get_users
from connect.user.delete_user import delete_users
from connect.login.login import login
from helpers.jwt import encode_jwt
from middelwars.token_required import token_required


app = Flask(__name__, static_url_path='/static')


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/api/user",  methods=["GET", "POST", "DELETE"])
# Работа с сущностью пользователь
def user():
    print("work api user ", request.method)

    if request.method == "GET":
        res = get_users()
        return make_response(jsonify(res["data"]), res["code"])

    if request.method == "POST":
        user = request.form
        user_id = uuid.uuid4().hex
        res = create_user(
            user_id, user["name"], user["description"], user["role"], user["password"])
        return make_response(jsonify(res["data"]), res["code"])

    if request.method == "DELETE":
        user = request.get_json()
        res = delete_users(user["id"])
        return make_response(jsonify(res["data"]), res["code"])


@app.route("/api/login",  methods=["POST"])
# Работа с сущностью аутентификация
def login_handler():
    print("work api login ", request.method)

    if request.method == "POST":
        user = request.form
        res = login(user["name"], user["password"])
        if res["code"] != "200":
            return make_response(jsonify(res["data"]), res["code"])

        token = encode_jwt()
        if token:
            return make_response(jsonify({"token": token}), 200)
        else:
            return make_response(jsonify("Token is not created"), 500)


@app.route('/protected')
@token_required
def protected():
    return make_response(jsonify("Это защищенный маршрут"), 200)


if __name__ == "__main__":
    app.run(port=7000, debug=True)
