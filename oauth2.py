from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from database.database_base import get_db
from sqlalchemy.orm import Session
from config import settings

# Secret-key -> openssl.exe rand -hex 32
# algorithm , expriation time
from schemas import TokenData
from database.models import User

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def create_access_token(data: dict):
    to_encode = data.copy()
    expire_datetime = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire_datetime})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        users_id: str = payload.get('user_id')
        if users_id is None:
            raise credentials_exception
        token_data = TokenData(id=users_id)
    except JWTError as error:
        raise credentials_exception
    return token_data


# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # credentials_exception = HTTPException(
    #     status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Could not validate credentials',
    #     headers={'WWW-Authenticate': 'Bearer'}
    # )
    # token = verify_access_token(token, credentials_exception)
    # user = db.query(User).filter(User.id == token.id).first()
    # return user.id if user else None

# Limitations:
#
# * Authentication / Authorization is not in the scope of this task
def get_current_user():
    return 1

