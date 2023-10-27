from fastapi import APIRouter, Depends, status, HTTPException
import fastapi as _fastapi
import logging
import sys
import fastapi.security as _security
from sqlalchemy.exc import SQLAlchemyError
from core import config
from db_models.crud.user import authenticate_user,register,get_user_by_email,get_hashed_token,create_hashed_token,edit_confirmed_status
from db_models.crud.email import request_email_confirmation_link,request_password_reset_link
from schema_models import user_schema
from sqlalchemy.orm import Session
from auth.permissions import AuthHandler
from custom_errors import exceptions as onbording_exceptions

logger = logging.getLogger()

auth_handler = AuthHandler()
router = APIRouter(
    prefix="/user",
    tags=['Users']
)


@router.post('/register', status_code=201, response_model=user_schema.ShowCurrentUser)
async def register_user(request: user_schema.UserCreate, db: Session = Depends(config.get_db)):
    try:
        user = await register(request, db)
    except (onbording_exceptions.EmailExist):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    except SQLAlchemyError as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"something is wrong with your query")
    except:
        logger.error("Unexpected Error:", sys.exc_info())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return user




@router.post("/login")
async def generate_token(
        form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(),
        db: Session = Depends(config.get_db),
):
    try:
        user = await authenticate_user(form_data.username, form_data.password, db)

    except (onbording_exceptions.UserNotFound, onbording_exceptions.PasswordMismatch):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    token = auth_handler.encode_token(user.id)
    return {'token': token}



@router.post('/email-verification',
             response_model=None,
             status_code=status.HTTP_202_ACCEPTED,
             operation_id='email_verification',
             tags=['email'])
async def send_email_verification_link(
        email: str,
        db: Session = Depends(config.get_db)
) -> None:
    """Endpoint for email verification
     Args:
        email: Recipient email address
    """
    if not email:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Email cannot be empty")
    user_obj = await get_user_by_email(email, db)
    if user_obj is not None:
        await request_email_confirmation_link(db,email)
    else:
        logger.debug("Email not found: %s")


@router.post('/password-reset',
             response_model=None,
             operation_id='password_reset',
             tags=['email'])
async def send_password_reset_link(
        email: str,
        db: Session = Depends(config.get_db)
) -> None:
    """Endpoint for password reset
     Args:
        email: Recipient email address
    """
    if not email:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Email cannot be empty")
    user = await get_user_by_email(email, db)
    if user is not None:
        await request_password_reset_link(email)
    else:
        logger.debug("Email not found: %s")


@router.post("/verify-email")
async def verify_email(token: str,db:Session=Depends(config.get_db)):
    hashed_token = auth_handler.generate_and_hash_token(token)
    db_token     = get_hashed_token(db, hashed_token)
    if not db_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid code")
    user_obj = await get_user_by_email(db_token.email, db)
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User does not exist")
    if user_obj.verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Email can only be verified once')
    await edit_confirmed_status(user_obj.id,True,db)

    return {
        "status": "success",
        "message": "Account verified successfully"
    }







    # if not confirmation:
    #     raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Token mismatch")

    return {"message": "Email verification successful"}