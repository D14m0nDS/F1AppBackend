import secrets

def make_key(length: int = 32) -> str:

    return secrets.token_urlsafe(length)

if __name__ == "__main__":
    print("SECRET_KEY="     + make_key(32))
    print("JWT_SECRET_KEY=" + make_key(32))
