from functools import wraps
from flask import Flask, request, render_template, jsonify, make_response
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
        return make_response(jsonify(res["data"]), res["code"])


# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         auth = request.headers.get('Authorization')

#         if not auth:
#             return make_response('Токен не предоставлен', 401, {'WWW-Authenticate': 'Bearer realm="Login Required"'})

#         try:
#             token_type, token = auth.split()
#             if token_type.lower() != 'bearer':
#                 return make_response('Неправильный формат токена', 401, {'WWW-Authenticate': 'Bearer realm="Login Required"'})
#         except ValueError:
#             return make_response('Неправильный формат токена', 401, {'WWW-Authenticate': 'Bearer realm="Login Required"'})

#         # if token not in users.values():
#         #     return make_response('Неверный токен', 401, {'WWW-Authenticate': 'Bearer realm="Login Required"'})

#         return f(*args, **kwargs)

#     return decorated


# @app.route('/protected')
# @token_required
# def protected():
#     return jsonify({'message': 'Это защищенный маршрут'})


if __name__ == "__main__":
    app.run(debug=True)
