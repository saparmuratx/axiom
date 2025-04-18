import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.x509 import load_pem_x509_certificate
from pathlib import Path


def validate_jwt(token: str, path_to_key):
    public_key_text = Path(path_to_key).read_text()

    print(public_key_text)

    public_key = load_pem_x509_certificate(public_key_text.encode('utf-8')).public_key()

    return jwt.decode(jwt=token, key=public_key, algorithms="RS256", audience=["http://localhost:8000"])


if __name__ == "__main__":
    token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2F4aW9tYWUueHl6Iiwic3ViIjoiYTI3MTQ3ZGUtZTFlZC00OTI1LWFmYjUtZmI5NDBmYjIzMGVlIiwiYXVkIjoiaHR0cDovL2xvY2FsaG9zdDo4MDAwIiwiaWF0IjoxNzQ0OTU4OTIyLjA0MDAzOCwiZXhwIjoxNzQ1MDQ1MzIyLjA0MDAzOCwic2NvcGUiOiJhdXRoIn0.Nhjp7CR_2QUgF9-aaO2DrBjxvurji7q6FNzh8ktUWMechKeWrcSvMGF1Z7NWY4oDgaq6fCA9IuJd215vKrOR9fUaMuN6dNLRCzMjJkhxt23tfwoJvFP8NNWK2hLCnfeSWBNmTdAMznxWFqfrdxSl6QeuVizNLxHPMecsg3229n-Tk6n7-cWpGP2TQfC8hduV7AFiKuFrKMEcka0R6BXUHGIA0nku5VwkdmTIIe6fattfPcgYWadeuRlTiCggzItztaWP3iAp2bMYqp2mhjBgLGs2lpXjhKlie2qJCknWtZs-tAi1FcqLDodtrgYzA3iDffyurZt57YUtCALot_6OUg"

    path_to_key = "keys/public_key.pem"

    is_valid = validate_jwt(token=token, path_to_key=path_to_key)

    print(is_valid)
