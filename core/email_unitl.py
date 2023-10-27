import logging
from datetime import date
from core.settings import get_email_credentials
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from jinja2 import Environment, select_autoescape, PackageLoader
from schema_models.user_schema import *


env = Environment(
    loader=PackageLoader('email_templates', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


logger = logging.getLogger(__name__)
settings = get_email_credentials()

class EmailClient:
    """EmailClient, Native Email Client using aiosmtplib, help to send emails, and confirm emails, also if the user forgot his password."""

    def __init__(
            self,
            username: str,
            password: str,
            host: str,
            tls: bool,
            base_url: str,
            site: str,
            display_name: str,
    ):
        self._username = username
        self._password = password
        self._host = host
        self._tls = tls
        self._base_url = base_url
        self._site = site
        self._display_name = display_name

    async def _send_email(self, email: str, subject: str, message: str) -> None:
        print('sending email........')
        print(self._tls)
        print(self._username)
        print(settings)
        print(settings["MAIL_FROM"])

        message = MessageSchema(
            subject=subject,
            recipients=[email],
            body=message,
            subtype="html"
        )

        # Define the config
        conf = ConnectionConfig(
            MAIL_USERNAME=self._username,
            MAIL_PASSWORD=self._password,
            MAIL_FROM=settings["MAIL_FROM"],
            MAIL_PORT=settings["MAIL_PORT"],
            MAIL_SERVER=settings["MAIL_SERVER"],
            MAIL_STARTTLS=False,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True
        )

        fm = FastMail(conf)

        try:
            await fm.send_message(message)
        except Exception as e:
            logger.msg('Error sending email notification: %s' % (str(e)), 'NOTIFICATIONS')
            return 1

        print('email Sent........')


    async def email_template(self,template,subject,url,username) -> None:
        # Generate the HTML template base on the template name
        template = env.get_template(f'{template}.html')
        full_url = self._base_url + url
        html = template.render(
            url=full_url,
            first_name=username,
            subject=subject
        )

        return html


    async def email_verification_link(self,secret_string: str) -> None:
        url=f"""/email-verification?token={secret_string}"""
        full_url = self._base_url + url
        return full_url

    async def password_reset_link  (self,secret_string: str) -> None:
        url = f"""/password-reset?token={secret_string}"""
        full_url = self._base_url + url
        return full_url

    async def send_email_verification_link(self,email,secret_string,username) -> None:
        """Sends email, with the generated link in the email body."""
        message = Mail(
            from_email=settings["MAIL_FROM"],
            to_emails=email,
        )
        message.dynamic_template_data = {
            'subject': 'Verify your email',
            'name': username,
            'emailVerificationLink': await self.email_verification_link(secret_string),
            'copyright': date.today().year
        }
        message.template_id = settings["EMAIL_VERIFICATION_TEMPLATE"]
        if not settings["SENDGRID_API_KEY"]:
            raise ValueError('no sendgrid credentials available')
        sendgrid_client = SendGridAPIClient(settings["SENDGRID_API_KEY"])
        response = sendgrid_client.send(message)
        if response.status_code != 202:
            raise Exception("Failed to send e-mail message to SendGrid")

    async def send_password_reset_link(self,email,secret_string,username) -> None:
        """Sends email, with the generated link in the email body."""
        message = Mail(
            from_email=settings.from_email,
            to_emails=email,
        )
        message.dynamic_template_data = {
            'subject': 'Password Reset',
            'name': username,
            'passwordResetLink': await self.password_reset_link(secret_string),
            'copyright': date.today().year
        }
        message.template_id = settings["PASSWORD_RESET_TEMPLATE"]
        if not settings["SENDGRID_API_KEY"]:
            raise ValueError('no sendgrid credentials available')
        sendgrid_client = SendGridAPIClient(settings["SENDGRID_API_KEY"])
        response = sendgrid_client.send(message)
        if response.status_code != 202:
            raise Exception("Failed to send e-mail message to SendGrid")












































































































































































































































































































































































































