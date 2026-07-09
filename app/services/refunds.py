"""Refund bookkeeping.

When a booking is cancelled a refund is calculated from its price and the
applicable notice tier, then written to the refund ledger with a processed
status. Amounts are stored in whole cents.
"""
import math
from datetime import datetime

from sqlalchemy.orm import Session

from ..models import Booking, RefundLog


def calculate_refund_amount(price_cents: int, percent: int) -> int:
    """Round to the nearest cent with half-cents rounding up."""
    return math.floor(price_cents * percent / 100.0 + 0.5)


def log_refund(db: Session, booking: Booking, amount_cents: int) -> RefundLog:
    entry = RefundLog(
        booking_id=booking.id,
        amount_cents=amount_cents,
        status="processed",
        processed_at=datetime.utcnow(),
    )
    db.add(entry)
    return entry
