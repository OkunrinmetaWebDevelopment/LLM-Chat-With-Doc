from core.email_unitl import EmailClient
from core.settings import get_email_credentials
from auth.permissions import AuthHandler
from db_models.crud.user import create_hashed_token,get_user_by_email
from sqlalchemy.orm import Session



auth_handler = AuthHandler()


def _create_email_client():
    settings = get_email_credentials()

    return EmailClient(
            settings["MAIL_USERNAME"],
            settings["MAIL_PASSWORD"],
            settings["MAIL_SERVER"],
            settings["MAIL_PORT"],
            settings["BASE_URL"],
            settings["SITE"],
            settings["DISPLAY_NAME"],
    )


async def request_email_confirmation_link(db:Session,email: str) -> None:
        token = auth_handler.create_secret_string()
        create_hashed_token(db,email,token[1])
        user_obj = await get_user_by_email(email, db)
        email_client = _create_email_client()
        await email_client.send_email_verification_link(email, token[0],user_obj.username)


async def request_password_reset_link(db:Session,email: str) -> None:
    token = auth_handler.create_secret_string()
    create_hashed_token(db,email,token[1])
    user_obj = await get_user_by_email(email, db)
    email_client = _create_email_client()
    await email_client.send_password_reset_link(email, token[0],user_obj.username)

