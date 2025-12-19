import bcrypt
from sqlalchemy.exc import IntegrityError
from src.models import User, Role
from src.utils import AlreadyExists, NotFound, AuthenticationError, ValidationError


class UserService:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(User).all()

    def get_by_id(self, user_id):
        user = self.session.query(User).get(user_id)
        if not user:
            raise NotFound(f"User with ID {user_id} are not found")
        return user

    def get_by_email(self, email):
        return self.session.query(User).filter_by(email=email).first()

    def create(self, name, email, password, role=Role.CUSTOMER):
        if len(password) < 6:
            raise ValidationError("password should be more than 6 character")

        if self.get_by_email(email):
            raise AlreadyExists(f"Email {email} already registered")

        hashed = bcrypt.hashpw(password.encode(
            'utf-8'), bcrypt.gensalt()).decode('utf-8')
        user = User(name=name, email=email, password=hashed, role=role)

        self.session.add(user)
        self.session.flush()
        return user

    def update(self, user_id, data: dict):
        user = self.get_by_id(user_id)

        if 'name' in data and data['name']:
            user.name = data['name']

        if 'role' in data and data['role']:
            user.role = data['role']

        if 'password' in data and data['password']:
            if len(data['password']) < 6:
                raise ValidationError(
                    "Password should be more than 6 character")
            hashed = bcrypt.hashpw(data['password'].encode(
                'utf-8'), bcrypt.gensalt()).decode('utf-8')
            user.password = hashed

        if 'email' in data and data['email'] != user.email:
            if self.get_by_email(data['email']):
                raise AlreadyExists(
                    f"Email {data['email']} already been used")
            user.email = data['email']

        self.session.add(user)
        return user

    def delete(self, user_id):
        user = self.get_by_id(user_id)

        self.session.delete(user)
        return {"message": "User deleted successfully"}

    def authenticate(self, email, password):
        user = self.get_by_email(email)

        if not user:
            raise AuthenticationError("Wrong Email or Password")

        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            raise AuthenticationError("Wrong Email or Password")

        return user

    def change_password_secure(self, user_id, old_password, new_password):
        user = self.get_by_id(user_id)

        if not bcrypt.checkpw(old_password.encode('utf-8'), user.password.encode('utf-8')):
            raise ValidationError("old password wrong")

        if len(new_password) < 6:
            raise ValidationError("new password requiring atleast 6 character")

        hashed = bcrypt.hashpw(new_password.encode(
            'utf-8'), bcrypt.gensalt()).decode('utf-8')
        user.password = hashed

        self.session.add(user)
        return {"message": "Password changed successfully"}
