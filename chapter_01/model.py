from dataclasses import dataclass
from datetime import date
from typing import List, Optional


class OutOfStock(Exception):
    pass


def allocate(line: "OrderLine", batches: List["Batch"]):
    try:
        batch = next(b for b in batches if b.can_allocate(line))
        batch.allocate(line)
        return batch.reference
    except StopIteration:
        raise OutOfStock(f"Out of stock for sku {line.sku}")


@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int


class Batch:
    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]):
        """
        Класс batch представляет партию товара
        :param ref: reference - артикул товара
        :param sku: stock keeping unit - наименование товара
        :param qty: quantity - количество заказа
        :param eta: expected time of arrival - время прибытия
        """
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self.available_quantity = qty
        self._allocations = set()

    def __repr__(self):
        return f"<Batch: {self.reference}>"

    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        return self.reference == other.reference

    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

    def allocate(self, line: OrderLine):
        """После проверки заказа, создает заказ"""
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)

    def can_allocate(self, line: OrderLine):
        return self.sku == line.sku and self.available_quantity >= line.qty
