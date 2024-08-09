import os
from pathlib import Path
from fastapi_mail import FastMail, MessageSchema, MessageType, ConnectionConfig
from fastapi.background import BackgroundTasks
from app.config.settings import get_settings


settings = get_settings()

conf = ConnectionConfig(
    MAIL_USERNAME=os.environ.get("MAIL_USERNAME"),
    MAIL_PASSWORD=os.environ.get("MAIL_PASSWORD"),
    MAIL_PORT=int(os.environ.get("MAIL_PORT", 1025)), 
    MAIL_SERVER=os.environ.get("MAIL_SERVER", "smtp"),
    MAIL_STARTTLS=os.environ.get("MAIL_STARTTLS", False) in ["True", "1"],  
    MAIL_SSL_TLS=os.environ.get("MAIL_SSL_TLS", False) in ["True", "1"],  
    MAIL_FROM=os.environ.get("MAIL_FROM", 'noreply@test.com'),
    MAIL_FROM_NAME=os.environ.get("MAIL_FROM_NAME", settings.APP_NAME),
    TEMPLATE_FOLDER=Path(__file__).parent.parent / "templates",  
    USE_CREDENTIALS=os.environ.get("USE_CREDENTIALS", "True") in ["True", "1"], 
    SUPPRESS_SEND=settings.SUPPRESS_SEND,
)


fm = FastMail(conf)

async def send_email(email: str, subject: str, template_body: dict, template_name: str, background_tasks: BackgroundTasks):
    message = MessageSchema(
        subject=subject,
        recipients=[email],
        template_body=template_body,
        subtype=MessageType.html,
    )
    
    background_tasks.add_task(fm.send_message, message, template_name=template_name)
    
    return {"message": "Email sent!"}
