from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    # we need to create the hash of the password before creating the user
    return pwd_context.hash(password)

def verify_hashed_password(plain_pass , hashed_pass):
    return pwd_context.verify(plain_pass,hashed_pass)