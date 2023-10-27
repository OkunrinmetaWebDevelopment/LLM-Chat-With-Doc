from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from schema_models import user_schema
from auth.permissions import AuthHandler
from db_models.crud.user import get_user_by_id
from core import config
from custom_errors import  exceptions as onbording_exceptions


auth_handler = AuthHandler()

async def get_current_user(user=Depends(auth_handler.auth_wrapper),db: Session=Depends(config.get_db))->user_schema.ShowCurrentUser:
    user = await get_user_by_id(user, db)
    if not user:
        raise onbording_exceptions.UserNotFound
    return user