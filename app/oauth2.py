from fastapi import Depends, security
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas

# provide the login endpoint
oauth2_scheme = security.OAuth2PasswordBearer(tokenUrl="login")
# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(payload: dict):
    payload_copy_to_encode = payload.copy()
    # expiry time = current time + 30 mins
    expiry_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # add expiration time to payload
    payload_copy_to_encode.update({"expiry_time": str(expiry_time)})

    new_encoded_jwt = jwt.encode(
        payload_copy_to_encode, SECRET_KEY, algorithm=[ALGORITHM]
    )
    return new_encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        # decode the token sent by the user to verify if the token is valid
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # from payload we get the user_id that we put in while sending a payload
        user_id = payload.get("user_id")

        if user_id is None:
            raise credentials_exception

        token_data = schemas.TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)):
    pass
