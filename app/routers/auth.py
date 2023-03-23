from fastapi import APIRouter, Depends, status, HTTPException, responses
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import schemas, models, database, utils
from app.routers import oauth2

router = APIRouter(tags=["Authentication"])



# user will send data, so its a post request
@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    # username, password - only theses fields will be retrieved from the OAuth2PasswordRequestForm so we cannot compare it to the email
    # we also have to make changes in Postman, instead of using Body we have to insert data in form-data

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}