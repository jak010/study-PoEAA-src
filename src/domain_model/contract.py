from __future__ import annotations

from typing import List

from .mfdate import MfDate
from .money import Money
from .product import Product
from .revenue_recognition import RevenueRecognition


class Contract:

    def __init__(self, product: Product, revenue: Money, when_signed: MfDate):
        self._id: int = None
        self._revenue_recognitions: List[RevenueRecognition] = []

        self._product = product
        self._money = revenue
        self._when_signed = when_signed

    def recognized_revenue(self, asof) -> Money:
        result = Money.dollors(krw=0)

        for revenue_recognition in self._revenue_recognitions:
            if revenue_recognition.is_recognizable_by(asof):
                result += revenue_recognition.get_amount()

        return result

    def add_revenue_recognition(self, revenue_recognition: RevenueRecognition):
        self._revenue_recognitions.append(revenue_recognition)

    def get_revenue(self):
        return self._money

    def get_when_signed(self):
        return self._when_signed

    def calculate_recognitions(self):
        self._product.calculate_revenue_recognition(self)
