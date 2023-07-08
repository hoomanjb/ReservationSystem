from fastapi import status, HTTPException, Depends, APIRouter

from database.models import User
from database.database_base import get_db
from sqlalchemy.orm import Session

from schemas import Token
from utils import verify
from oauth2 import create_access_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'])


# OAuth2PasswordRequestForm -> username , password  -> send it form data
@router.post('/login', response_model=Token)
def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    my_user = db.query(User).filter(User.email == user.username).first()
    if not my_user or not verify(user.password, my_user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials"
        )
    access_token = create_access_token(data={'user_id': 1})
    return {'access_token': access_token, 'token_type': 'bearer'}

