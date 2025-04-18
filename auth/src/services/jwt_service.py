import jwt
from datetime import datetime

payload = {
    "iss": "https://auth.coffeemesh.io/",
    "sub": "ec7bbccf-ca89-4af3-82ac-b41e4831a962",
    "aud": "http://127.0.0.1:8000/orders",
    "iat": int(datetime.now().timestamp()),
    "exp": 1667238616,
    "azp": "7c2773a4-3943-4711-8997-70570d9b099c",
    "scope": "openid",
}


key = "this a key innit?"

token = jwt.encode(payload=payload, key=key, algorithm="HS256")


print(token)
