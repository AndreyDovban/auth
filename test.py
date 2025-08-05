from functools import wraps
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

# Заглушка для базы данных пользователей и токенов
users = {'user1': 'secret_token'}

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization')

        if not auth:
            return make_response('Токен не предоставлен', 401, {'WWW-Authenticate': 'Bearer realm="Login Required"'})

        try:
            token_type, token = auth.split()
            if token_type.lower() != 'bearer':
                return make_response('Неправильный формат токена', 401, {'WWW-Authenticate': 'Bearer realm="Login Required"'})
        except ValueError:
             return make_response('Неправильный формат токена', 401, {'WWW-Authenticate': 'Bearer realm="Login Required"'})


        if token not in users.values():
            return make_response('Неверный токен', 401, {'WWW-Authenticate': 'Bearer realm="Login Required"'})

        return f(*args, **kwargs)

    return decorated

@app.route('/protected')
@token_required
def protected():
    return jsonify({'message': 'Это защищенный маршрут'})

if __name__ == '__main__':
    app.run(debug=True)