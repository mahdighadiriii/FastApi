from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy.orm import Session

from .. import crud, database, dependencies, schemas

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=schemas.UserOut,
    summary="Register a new user",
    description="Create a new user with username and password.",
)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    existing_user = crud.users.get_user_by_username(db, username=user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.users.create_user(db, user)


@router.post(
    "/login",
    response_model=schemas.Token,
    summary="Login and get tokens",
    description="Login with username and password to receive access and refresh tokens in cookies.",
)
def login(
    response: Response,
    form_data: schemas.LoginForm,
    db: Session = Depends(database.get_db),
):
    user = crud.users.get_user_by_username(db, username=form_data.username)
    if not user or not crud.users.verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = dependencies.create_access_token(data={"sub": str(user.id)})
    refresh_token = dependencies.create_refresh_token(data={"sub": str(user.id)})
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        secure=False,
        samesite="strict",
        max_age=dependencies.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="strict",
        max_age=dependencies.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/refresh", response_model=schemas.Token, summary="Refresh access token", description="Use refresh token to get a new access token and refresh token.")
def refresh_token(
    response: Response,
    refresh_token: str | None = Cookie(None),
    db: Session = Depends(database.get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired refresh token",
    )
    if not refresh_token:
        print("No refresh token provided")  # برای دیباگ
        raise credentials_exception
    print(f"Received refresh token: {refresh_token}")  # برای دیباگ
    try:
        payload = jwt.decode(refresh_token, dependencies.SECRET_KEY, algorithms=[dependencies.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            print("No user_id in token")  # برای دیباگ
            raise credentials_exception
        print(f"Decoded user_id: {user_id}")  # برای دیباگ
    except jwt.JWTError as e:
        print(f"JWT decode error: {e}")  # برای دیباگ
        raise credentials_exception
    user = crud.users.get_user(db, user_id=int(user_id))
    if user is None:
        print("User not found")  # برای دیباگ
        raise credentials_exception
    access_token = dependencies.create_access_token(data={"sub": str(user.id)})
    new_refresh_token = dependencies.create_refresh_token(data={"sub": str(user.id)})
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        secure=False,  # برای تست localhost
        samesite="strict",
        max_age=dependencies.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=False,  # برای تست localhost
        samesite="strict",
        max_age=dependencies.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    )
    return {"access_token": access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}


@router.post(
    "/logout",
    summary="Logout user",
    description="Clear access and refresh tokens from cookies.",
)
def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Logged out successfully"}
