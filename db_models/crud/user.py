from fastapi import status, HTTPException,Response
import sys
import logging
from email_validator import EmailNotValidError, validate_email
from sqlalchemy.orm import Session
from db_models.models import User,HashedToken
from sqlalchemy.exc import SQLAlchemyError
from auth.permissions import AuthHandler
from custom_errors import  exceptions as onbording_exceptions
from schema_models.user_schema import *




logger = logging.getLogger()
auth_handler = AuthHandler()


def create_user(user: UserCreate, db: Session):
    try:
        user_obj =User(
        username=user.username,
        email=user.email,
        hashed_password= auth_handler.get_password_hash(user.hashed_password)
        )
        db.add(user_obj)
        db.commit()
        db.flush()
        db.refresh(user_obj)
    except SQLAlchemyError as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"something is wrong with your query")
    except:
        logger.error("Unexpected Error:", sys.exc_info())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return user_obj


async def register(request:UserCreate,db:Session):
    try:
        validate_email(request.email, timeout=5)
    except EmailNotValidError as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Email format"
        )

    if await get_user_by_email(request.email, db):
        raise onbording_exceptions.EmailExist

    user = create_user(request, db)

    return user



async def get_user_by_email(email: str, db: Session):
    try:
        new_user = db.query(User).filter(User.email == email).first()

    except SQLAlchemyError as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"something is wrong with your query")
    except:
        logger.error("Unexpected Error:", sys.exc_info())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return new_user



async def get_user_by_username(username: str, db: Session):
    try:
        new_user = db.query(User).filter(User.username == username).first()
        return new_user

    except SQLAlchemyError as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"something is wrong with your query")
    except:
        logger.error("Unexpected Error:", sys.exc_info())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)



async def get_user_by_id(id: int, db: Session)->ShowCurrentUser:
    try:
        new_user = db.query(User).filter(User.id == id).first()
        print(new_user.__dict__)
        return ShowCurrentUser.from_orm(new_user)

    except SQLAlchemyError as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"something is wrong with your query")
    except:
        logger.error("Unexpected Error:", sys.exc_info())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#
#
async def authenticate_user(email: str, password: str, db:Session):
    user = await get_user_by_email(db=db, email=email)
    if not user:
        raise onbording_exceptions.UserNotFound
    if not auth_handler.verify_password(password, user.hashed_password):
        raise onbording_exceptions.PasswordMismatch
    return user


async def edit_confirmed_status(id: int, confirmed_status: bool, db: Session):
    try:
        edited_status = db.query(User).filter(User.id == id)
        if not edited_status.first():
            raise onbording_exceptions.UserNotFound
        edited_status.update({"verified": confirmed_status})
        db.commit()

    except SQLAlchemyError as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"something is wrong with your query")
    except:
        logger.error("Unexpected Error:", sys.exc_info())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return edited_status



def create_hashed_token(db: Session, email,hashed_token: str):
    db_token = HashedToken(email=email,hashed_token=hashed_token)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token


def get_hashed_token(db: Session, hashed_token: str):
    db_token = db.query(HashedToken).filter(HashedToken.hashed_token == hashed_token).first()
    return db_token










