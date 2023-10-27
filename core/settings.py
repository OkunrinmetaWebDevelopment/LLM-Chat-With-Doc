from decouple import config


def get_db_credentials():
    settings={
        'POSTGRES_USER':config("POSTGRES_USER"),
        'POSTGRES_PASSWORD':config("POSTGRES_PASSWORD"),
        'POSTGRES_SERVER':config("POSTGRES_SERVER"),
        'POSTGRES_PORT':config("POSTGRES_PORT"),
        'POSTGRES_DB':config("POSTGRES_DB"),
        }
    return settings



def get_email_credentials():
    settings={
        'MAIL_USERNAME':config("MAIL_USERNAME"),
        'MAIL_PASSWORD':config("MAIL_PASSWORD"),
        'MAIL_PORT':config("MAIL_PORT"),
        'MAIL_FROM': config("MAIL_FROM"),
        'MAIL_SERVER':config("MAIL_SERVER"),
        'MAIL_TLS':config("MAIL_TLS"),
        'MAIL_SSL': config("MAIL_TLS"),
        'USE_CREDENTIALS': config("MAIL_TLS"),
        'BASE_URL': config("BASE_URL"),
        'DISPLAY_NAME': config("DISPLAY_NAME"),
        'SITE': config("SITE"),
        'SENDGRID_API_KEY': config("SENDGRID_API_KEY"),
        'PASSWORD_RESET_TEMPLATE': config("PASSWORD_RESET_TEMPLATE"),
        'EMAIL_VERIFICATION_TEMPLATE': config("EMAIL_VERIFICATION_TEMPLATE"),
        }
    return settings


def get_ai_credentials():
    settings={
        'OPENAI_API_KEY':config("OPENAI_API_KEY"),
        'HUGGINGFACEHUB_API_TOKEN':config("HUGGINGFACEHUB_API_TOKEN"),
        'CEREBRIUMAI_API_KEY':config("CEREBRIUMAI_API_KEY"),
        }
    return settings
