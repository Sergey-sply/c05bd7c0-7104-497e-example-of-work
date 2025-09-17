from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from mail_domain_service.infrastructure.database.db import async_session_maker_ctx
from mail_domain_service.infrastructure.repositories.mailbox import MailRepository
from mail_domain_service.infrastructure.schemas.mailbox import Mailbox
from mail_domain_service.infrastructure.services.decorators.session import use_session


class MailService:
    def __init__(self, mail_repository: MailRepository):
        self.mail_repository = mail_repository
        self._session_maker = async_session_maker_ctx.get()

    @use_session
    async def get_mail_data(self, order_id: UUID, session: AsyncSession | None = None) -> Mailbox | None:
        mail_service_ids = await self.mail_repository.get_mailorder_data(order_id, session)
        service_data = await self.mail_repository.get_service_data(
            service_id=mail_service_ids.service_id,
            session=session
        )
        mail_data = await self.mail_repository.get_mailbox_data(mail_id=mail_service_ids.mail_id, session=session)

        return Mailbox(
            id=mail_service_ids.mail_id,
            order_id=str(order_id),
            address=mail_data.address,
            password=mail_data.password,
            provider=mail_data.provider,
            folders=mail_data.folders,
            senders=service_data.senders,
            creds=mail_data.creds
        )

