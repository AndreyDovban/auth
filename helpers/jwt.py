import jwt
import datetime
import os

SECRET_KEY = os.getenv("SECRET_KEY")


def encode_jwt():
    payload = {
        "exp": datetime.datetime.now() + datetime.timedelta(hours=120, minutes=30)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def decode_jwt(token):
    return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
