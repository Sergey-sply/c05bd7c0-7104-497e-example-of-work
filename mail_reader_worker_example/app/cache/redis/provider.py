from typing import Optional

from .client import get_redis
from .result_publisher import ResultPublisher

_publisher: Optional[ResultPublisher] = None

async def get_publisher() -> ResultPublisher:
    global _publisher
    if _publisher is None:
        r = await get_redis()
        _publisher = ResultPublisher(r, 180)
    return _publisher

def reset_publisher():
    global _publisher
    _publisher = None