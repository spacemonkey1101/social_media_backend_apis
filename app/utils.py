from passlib.context import CryptContext


def hash(password: str):
    # we need to create the hash of the password before creating the user
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)
