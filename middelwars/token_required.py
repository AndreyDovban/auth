from functools import wraps
from flask import request, jsonify, make_response
import datetime
from helpers.jwt import decode_jwt


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

        decoded_payload = decode_jwt(token)
        print(f"Decoded payload: {decoded_payload}")

        if datetime.datetime.now() > datetime.datetime.fromtimestamp(decoded_payload["exp"]):
            print("TOKEN EXPIRES")
            return make_response(jsonify('Неверный токен'), 401, {'WWW-Authenticate': 'Bearer realm="Login Required"'})

        # res = get_user_by_name(decoded_payload["name"])
        # if res["code"] != "200":
        #     print("USER NOT FOUND")
        #     return make_response(jsonify('Неверный токен'), 401, {'WWW-Authenticate': 'Bearer realm="Login Required"'})

        # if res["data"][3] != "admin":
        #     print("PRMISSIO DENIED")
        #     return make_response(jsonify('Неверный токен'), 401, {'WWW-Authenticate': 'Bearer realm="Login Required"'})

        # if token not in users.values():
        #     return make_response('Неверный токен', 401, {'WWW-Authenticate': 'Bearer realm="Login Required"'})

        return f(*args, **kwargs)

    return decorated
