from typing import Any
import jwt

from pathlib import Path

from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.primitives import serialization


class JWTService:
    def __init__(
        self,
        algorithm: str = "HS256",
        secret_key: str = None,
        private_key_path: str = None,
        public_key_path: str = None,
    ):
        if algorithm not in (
            "HS256",
            "RS256",
        ):
            raise ValueError(f"Algorithm `{algorithm}` is not supported")

        self.algorithm = algorithm

        if algorithm == "HS256":
            if not secret_key:
                raise ValueError("secret_key is required for HS256 algorithm")

            self.secret_key = secret_key

        elif algorithm == "RS256":
            if not private_key_path or not public_key_path:
                raise ValueError(
                    "Both private_key and public_key are required for RS256 algorithm"
                )

            self.private_key = private_key_path
            self.public_key = public_key_path

    def get_secret_key(self):
        if self.algorithm == "RS256":
            private_key_text = Path(self.private_key).read_text()

            private_key = serialization.load_pem_private_key(
                private_key_text.encode(), password=None
            )

            return private_key
        elif self.algorithm == "HS256":
            return self.secret_key

    def get_public_key(self):
        if self.algorithm == "RS256":
            public_key_text = Path(self.public_key).read_text()

            public_key = load_pem_x509_certificate(
                public_key_text.encode("utf-8")
            ).public_key()

            return public_key
        elif self.algorithm == "HS256":
            return self.secret_key

    def generate_token(self, payload: dict) -> str:
        secret_key = self.get_secret_key()

        token = jwt.encode(algorithm=self.algorithm, payload=payload, key=secret_key)

        return token

    def validate_token(self, token, aud: list[str] = None) -> dict[str, Any]:
        public_key = self.get_public_key()

        res = jwt.decode(
            jwt=token, key=public_key, algorithms=[self.algorithm], audience=aud
        )

        return res
