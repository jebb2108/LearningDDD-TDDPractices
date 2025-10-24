from datetime import date, timedelta
import pytest

from model import Batch, OrderLine
from exc import (  # Импортируем исключения для тестов
    NotEnoughQuantityError,
    AvailableEqualToRequiredError,
    PrefersWarehouseToShipmentError,
    PrefersEarlierBatchesError,
)

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)

def test_allocating_to_a_batch_reduces_the_available_quantity():
    # Успешная аллокация: уменьшает количество
    batch = Batch("batch_0", "SMALL-widget", 20, eta=today)  # eta=today — в складе
    line = OrderLine("order_0", "SMALL-widget", 2)
    batch.allocate(line)
    assert batch.available_quantity == 18

def test_can_allocate_if_available_greater_than_required():
    # Успешная аллокация: available > required
    batch = Batch("batch_1", "LARGE-table", 15, eta=today)  # qty=15 > line.qty=10
    line = OrderLine("order_1", "LARGE-table", 10)
    batch.allocate(line)
    assert batch.available_quantity == 5

def test_cannot_allocate_if_available_smaller_than_required():
    # Неудачная аллокация: available < required → исключение
    batch = Batch("batch_2", "SMALL-widget", 5, eta=today)
    line = OrderLine("order_2", "SMALL-widget", 6)
    with pytest.raises(NotEnoughQuantityError):
        batch.allocate(line)
    # Количество не изменяется
    assert batch.available_quantity == 5

def test_can_allocate_if_available_equal_to_required():
    # Неудачная аллокация: available == required → исключение (по вашей логике в model.py)
    batch = Batch("batch_3", "MEDIUM-desk", 3, eta=today)
    line = OrderLine("order_3", "MEDIUM-desk", 3)
    with pytest.raises(AvailableEqualToRequiredError):
        batch.allocate(line)
    assert batch.available_quantity == 3

def test_prefers_warehouse_batches_to_shipments():
    # Неудачная аллокация: eta=tomorrow (в доставке) → исключение
    batch = Batch("batch_4", "SMALL-chairs", 30, eta=tomorrow)
    line = OrderLine("order_4", "SMALL-chairs", 10)
    with pytest.raises(PrefersWarehouseToShipmentError):
        batch.allocate(line)
    assert batch.available_quantity == 30

def test_prefers_earlier_batches():
    # Неудачная аллокация: eta=later (далеко в будущем) → исключение
    batch = Batch("batch_5", "SMALL-table", 10, eta=later)
    line = OrderLine("order_5", "SMALL-table", 9)
    with pytest.raises(PrefersEarlierBatchesError):
        batch.allocate(line)
    assert batch.available_quantity == 10
