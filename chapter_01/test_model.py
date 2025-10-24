from datetime import date, timedelta
import pytest

from model import Batch, OrderLine

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)

def make_batch_and_line(sku, batch_qty, line_qty):
    return (
        Batch("batch-001", sku, batch_qty, None),
        OrderLine("order-123", sku, line_qty)
    )

def test_allocating_to_a_batch_reduces_the_available_quantity():
    # Успешная аллокация: уменьшает количество
    large_batch, small_line = make_batch_and_line("ELEGANT-lamp", 20, 2)
    assert large_batch.can_allocate(small_line)

def test_cannot_allocate_if_available_smaller_than_required():
    # Неудачная аллокация: available < required → исключение
    small_batch, large_line = make_batch_and_line("ELEGANT-lamp", 2, 20)
    assert small_batch.can_allocate(large_line) is False

def test_can_allocate_if_available_equal_to_required():
    # Неудачная аллокация: available == required → исключение (по вашей логике в model.py)
    eq_batch, eq_line = make_batch_and_line("WOODEN-table", 10, 10)
    assert eq_batch.can_allocate(eq_line)

def test_cannot_allocate_if_sku_do_not_match():
    batch = Batch("batch-001", "ELEGANT-lamp", 10, today)
    line = OrderLine('order-123', "WOODEN-table", 2)
    assert batch.can_allocate(line) is False