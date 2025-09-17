from pydantic import BaseModel
from datetime import datetime

class MailMessage(BaseModel):
    status: str
    subject: str | None
    body: str | None
    date: datetime | None
