import os
import jwt
from datetime import datetime, timedelta, timezone
from pyramid.request import Request
from src.utils import AuthenticationError

SECRET_KEY = os.getenv("JWT_SECRET", "fallback_secret")
ALGORITHM = "HS256"


def create_access_token(user_id: int):
    expire = datetime.now(timezone.utc) + timedelta(hours=24)
    payload = {
        "sub": str(user_id),
        "exp": expire
    }
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user_id(request: Request) -> int:
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        raise AuthenticationError(
            "Authorization Header missing")

    try:
        scheme, token = auth_header.split()
        if scheme.lower() != 'bearer':
            raise AuthenticationError(
                "Token format wrong. Use 'Bearer <token>'")

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")

        if user_id is None:
            raise AuthenticationError("User ID missing")

        return int(user_id)

    except (ValueError, jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        raise AuthenticationError("Token expired or invalid")
