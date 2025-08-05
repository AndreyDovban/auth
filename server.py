from functools import wraps
from flask import Flask, request, render_template, jsonify, make_response
import uuid
from connect.user.create_user import create_user
from connect.user.get_users import get_users
from connect.user.delete_user import delete_users
from connect.login.login import login
from connect.user.get_user_by_name import get_user_by_name
import jwt
import datetime


# Секретный ключ
secret_key = "your-secret-key"

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
        print("Name ", res["data"][1])
        exp = datetime.datetime.now() + datetime.timedelta(minutes=30)
        print("EXP ", exp.strftime("%Y-%m-%d %H:%M:%S"))
        payload = {
            "name": res["data"][1],
            "role": res["data"][3],
            # Токен истекает через 30 минут
            "exp": exp
        }
        # Кодирование токена
        encoded_jwt = jwt.encode(payload, secret_key, algorithm="HS256")
        print(f"Encoded JWT: {encoded_jwt}")
        decoded_payload = jwt.decode(
            encoded_jwt, secret_key, algorithms=["HS256"])
        print(f"Decoded payload: {decoded_payload}")
        if res["code"] != "200":
            return make_response(jsonify(res["data"]), res["code"])
        return make_response(jsonify({"token": encoded_jwt}), 200)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization')

        if not auth:
            print("NOT AUTH")
            return make_response(jsonify('Токен не предоставлен'), 401, {'WWW-Authenticate': 'Bearer realm="Login Required"'})

        try:
            token_type, token = auth.split()
            if token_type.lower() != 'bearer':
                print("NOT BREARE")
                return make_response(jsonify('Неправильный формат токена'), 401, {'WWW-Authenticate': 'Bearer realm="Login Required"'})
        except ValueError:
            print("VALUE ERROR")
            return make_response(jsonify('Неправильный формат токена'), 401, {'WWW-Authenticate': 'Bearer realm="Login Required"'})

        decoded_payload = jwt.decode(
            token, secret_key, algorithms=["HS256"])
        print(f"Decoded payload: {decoded_payload}")

        if datetime.datetime.now() > decoded_payload["exp"]:
            print("TOKEN EXPIRES")
            return make_response(jsonify('Неверный токен'), 401, {'WWW-Authenticate': 'Bearer realm="Login Required"'})

        res = get_user_by_name(decoded_payload.name)
        if res["code"] != "200":
            print("USER NOT FOUND")
            return make_response(jsonify('Неверный токен'), 401, {'WWW-Authenticate': 'Bearer realm="Login Required"'})

        if res["data"][3] != "admin":
            print("PRMISSIO DENIED")
            return make_response(jsonify('Неверный токен'), 401, {'WWW-Authenticate': 'Bearer realm="Login Required"'})

        # if token not in users.values():
        #     return make_response('Неверный токен', 401, {'WWW-Authenticate': 'Bearer realm="Login Required"'})

        return f(*args, **kwargs)

    return decorated


@app.route('/protected')
@token_required
def protected():
    return make_response(jsonify("Это защищенный маршрут"), 200)


if __name__ == "__main__":
    app.run(debug=True)
