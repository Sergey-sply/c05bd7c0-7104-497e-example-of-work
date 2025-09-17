from typing import Protocol

from mail_reader_worker_example.app.schemas.mail import Mailbox, MailboxMessage


class MailProvider(Protocol):
    async def fetch_latest(self, mailbox: Mailbox) -> MailboxMessage | None: ...