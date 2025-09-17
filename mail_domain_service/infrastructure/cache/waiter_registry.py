import asyncio

WAITERS_CAP = 10_000

class WaiterRegistry:
    def __init__(self):
        self._waiters: dict[str, asyncio.Future] = {}

    def get_or_create(self, order_id: str) -> asyncio.Future | None:
        fut = self._waiters.get(order_id)
        if fut is None or fut.done():
            if len(self._waiters) >= WAITERS_CAP:
                return None
            fut = asyncio.get_event_loop().create_future()
            self._waiters[order_id] = fut
        return fut

    def resolve(self, order_id: str, payload: dict):
        fut = self._waiters.pop(order_id, None)
        if fut and not fut.done():
            fut.set_result(payload)


waiters = WaiterRegistry()
