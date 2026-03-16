import jwt
import datetime

SECRET = "SUPER_SECRET_KEY"
ALGO = "HS256"


def create_token(data: dict):

    payload = data.copy()

    payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(hours=6)

    token = jwt.encode(payload, SECRET, algorithm=ALGO)

    return token


def decode_token(token: str):

    try:
        data = jwt.decode(token, SECRET, algorithms=[ALGO])
        return data
    except:
        return None