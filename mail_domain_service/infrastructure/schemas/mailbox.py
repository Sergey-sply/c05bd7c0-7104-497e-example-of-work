from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class MailEnvelope(BaseModel):
    subject: str | None
    body: str | None
    date: datetime | None

class MailboxMessage(BaseModel):
    status: str
    result: str
    message: MailEnvelope | None

class Mailbox(BaseModel):
    id: int
    order_id: str
    address: str
    password: str
    provider: str
    folders: list[str]
    senders: list[str]
    creds: dict | None


class MailOrderDataSchema(BaseModel):
    id: UUID
    mail_id: int
    service_id: int

class ServiceDataSchema(BaseModel):
    id: int
    senders: list[str]

class MailboxDataSchema(BaseModel):
    id: int
    address: str
    password: str
    provider: str
    folders: list[str]
    creds: dict | None