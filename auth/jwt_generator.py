from datetime import datetime, timedelta
from multiprocessing import managers
from pathlib import Path
from uuid import uuid4

import jwt
from cryptography.hazmat.primitives import serialization

def generate_jwt():
    now = datetime.now()

    sub = uuid4()

    payload = {
        "iss": "https://axiomae.xyz",
        "sub": str(sub),
        "aud": "http://localhost:8000",
        "iat": now.timestamp(),
        "exp": (now + timedelta(hours=24)).timestamp(),
        "scope": "auth"
    }

    private_key_text = Path("keys/private_key.pem").read_text()

    private_key = serialization.load_pem_private_key(
        private_key_text.encode(),
        password=None
    )

    return jwt.encode(payload=payload, key=private_key, algorithm="RS256")


if __name__ == "__main__":
    token = generate_jwt()

    print(token)
