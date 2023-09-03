from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain_model.source.money import Money
    from src.domain_model.source.mfdate import MfDate


class RevenueRecognition:

    def __init__(self, amount: Money, date: MfDate):
        self.amount = amount
        self.date = date

    def get_amount(self):
        return self.amount

    def is_recognizable_by(self, asof: MfDate) -> bool:
        return asof.after(self.date) or asof.equals(self.date)

    def __repr__(self):
        return f"RevenueRecognition(" \
               f"amount={self.amount}, " \
               f"date={self.date}" \
               f")\n"
