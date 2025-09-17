from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class MailEnvelopeSchema(BaseModel):
    subject: str | None
    body: str | None
    date: datetime | None


class MailboxMessage(BaseModel):
    status: str
    result: str
    message: MailEnvelopeSchema | None

class Mailbox(BaseModel):
    id: int
    order_id: str
    address: str
    password: str
    provider: str
    folders: list[str]
    senders: list[str]
    creds: dict | None

Access = Literal["imap", "curl", "graph"]

class ProviderConfig(BaseModel):
    provider_access: Access
