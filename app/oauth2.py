from jose import JWTError, jwt
from datetime import datetime, timedelta

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(payload: dict):
    payload_copy_to_encode = payload.copy()
    # expiry time = current time + 30 mins
    expiry_time = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # add expiration time to payload
    payload_copy_to_encode.update({"expiry_time": expiry_time})

    new_encoded_jwt = jwt.encode(
        payload_copy_to_encode, SECRET_KEY, algorithm=ALGORITHM
    )
    return new_encoded_jwt
