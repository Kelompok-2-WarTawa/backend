from dataclasses import dataclass


@dataclass(frozen=True)
class RateLimitConfig:
    LIMIT: int = 100
    WINDOW: int = 60


@dataclass(frozen=True)
class EventConfig:
    SEATS_PER_ROW: int = 10


@dataclass(frozen=True)
class BookingConfig:
    MAX_TICKETS_PER_USER: int = 3


@dataclass(frozen=True)
class SecurityConfig:
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_HOURS: int = 24


rate_limit_settings = RateLimitConfig()
event_settings = EventConfig()
booking_settings = BookingConfig()
security_settings = SecurityConfig()
