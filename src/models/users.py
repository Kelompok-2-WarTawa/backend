from enum import Enum
from dataclasses import dataclass


class Role(Enum):
    ADMIN = "admin"
    USER = "user"


@dataclass
class User:
    id: int
    name: str
    email: str
    password: str
    role: Role
