import threading
from dataclasses import asdict, dataclass, field


@dataclass
class Order:
    order_id: str
    customer: str
    items: list
    amount: int
    status: str
    created_at: str
    updated_at: str


class OrderStore:
    def __init__(self):
        self._orders: dict[str, Order] = {}
        self._lock = threading.Lock()

    def create(self, order: Order) -> None:
        with self._lock:
            self._orders[order.order_id] = order

    def snapshot(self) -> list:
        with self._lock:
            return [asdict(order) for order in self._orders.values()]
