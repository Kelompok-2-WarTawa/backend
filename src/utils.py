from datetime import datetime, date
from decimal import Decimal
import enum


class AppError(Exception):
    def __init__(self, message, status_code=400, details=None):
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(message)


class NotFound(AppError):
    def __init__(self, message="Resource not found"):
        super().__init__(message, status_code=404)


class ValidationError(AppError):
    def __init__(self, message="Validation failed", details=None):
        super().__init__(message, status_code=400, details=details)


class AlreadyExists(AppError):
    def __init__(self, message="Resource already exists"):
        super().__init__(message, status_code=409)


class AuthenticationError(AppError):
    def __init__(self, message="Authentication required"):
        super().__init__(message, status_code=401)


def json_serializer(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, Decimal):
        return float(obj)
    if isinstance(obj, enum.Enum):
        return obj.value
    if hasattr(obj, '__table__'):
        return {c.name: (getattr(obj, c.name).value if isinstance(getattr(obj, c.name), enum.Enum) else getattr(obj, c.name)) for c in obj.__table__.columns}
    raise TypeError(f"Type {type(obj)} not serializable")
