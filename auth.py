import os
from os.path import join, dirname
from dotenv import load_dotenv
from datetime import timedelta, datetime
from jose import JWTError, jwt
from passlib.context import CryptContext

from schemas import TokenData

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(eval(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES')))

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: TokenData):
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode: TokenData = {
        "id": data.id,
        "name": data.name,
        "exp": expire
    }

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def validate_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return TokenData(**payload)
    except JWTError:
        return None