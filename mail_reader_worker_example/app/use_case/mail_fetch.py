from mail_reader_worker_example.app.provider.base import MailProvider
from mail_reader_worker_example.app.schemas.mail import Mailbox


class GetLatestMail:
    def __init__(self, provider_factory: callable):
        self.provider_factory = provider_factory

    async def execute(self, mailbox: Mailbox):
        mail_provider: MailProvider = self.provider_factory(mailbox.provider)
        mail = await mail_provider.fetch_latest(
            mailbox=mailbox
        )
        return mail