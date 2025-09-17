from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from mail_domain_service.infrastructure.repositories.base import BaseRepository
from mail_domain_service.infrastructure.schemas.mailbox import MailboxDataSchema, ServiceDataSchema, MailOrderDataSchema


class MailRepository(BaseRepository):

    async def get_mailbox_data(self, mail_id: int, session: AsyncSession) -> MailboxDataSchema | None:
        row = {}
        if row is None:
            return None

        return MailboxDataSchema(
            id=row["id"],
            address=row["address"],
            password=row["password"],
            provider=row["provider"],
            folders=row["folders"],
            creds=row["creds"],
        )

    async def get_service_data(self, service_id: int, session: AsyncSession) -> ServiceDataSchema | None:
        row = {}
        if not row:
            return None
        sid, senders = row
        return ServiceDataSchema(id=sid, senders=senders)

    async def get_mailorder_data(self, order_id: UUID, session: AsyncSession) -> MailOrderDataSchema | None:
        row = {}
        if row is None:
            return None
        mail_id, service_id = row

        return MailOrderDataSchema(
            id=order_id,
            mail_id=mail_id,
            service_id=service_id
        )