import os
import jwt
from datetime import datetime, timedelta, timezone
from pyramid.request import Request
from functools import wraps
from src.utils import AuthenticationError, AuthorizationError
from src.config.settings import security_settings

SECRET_KEY = os.getenv("JWT_SECRET")
if not SECRET_KEY:
    raise ValueError("FATAL: JWT_SECRET environment variable not set!")
ALGORITHM = security_settings.ALGORITHM


def create_access_token(user_id: int):
    expire = datetime.now(timezone.utc) + timedelta(hours=24)
    payload = {
        "sub": str(user_id),
        "exp": expire
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


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


def login_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        try:
            user_id = get_current_user_id(request)
        except AuthenticationError as e:
            raise e

        user = request.services.user.get_by_id(user_id)

        request.user = user

        return func(request, *args, **kwargs)
    return wrapper


def admin_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        user_id = get_current_user_id(request)
        user = request.services.user.get_by_id(user_id)

        from src.models import Role

        if user.role != Role.ADMIN:
            raise AuthorizationError("Access Denied: Admin Only")

        request.user = user

        return func(request, *args, **kwargs)
    return wrapper
