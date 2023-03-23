from jose import JWTError, jwt
from datetime import datetime, timedelta
from app import schemas, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.database import get_db
from sqlalchemy.orm import Session
from app.config import settings

# we have to insert here our login endpoint without the slash
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# SECRET KEY
# algorithm
# expiration time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        # decode jwt token
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        #extract id
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        # validate id with TokenData schema
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data
    

# we are going to get the current user from the login endpoint
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # it calls verify access token

    # what exception should be raised in case 
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Aythenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user