from mail_domain_service.infrastructure.schemas.mailbox import Mailbox
from mail_domain_service.infrastructure.taskiq.broker import broker


@broker.task(task_name="read_latest_task")
async def read_latest_task(payload: Mailbox) -> dict:
    """
    just pub task
    """
    return {"queued": True}