from __future__ import annotations

import copy
from typing import List, TYPE_CHECKING

from src.domain_model.source.money import Money

if TYPE_CHECKING:
    from src.domain_model.source.mfdate import MfDate

    from src.domain_model.source.revenue_recognition import RevenueRecognition
    from src.domain_model.source.product import Product


class Contract:

    def __init__(self, product: Product, revenue: Money, when_signed: MfDate):
        self._id: int = None
        self._revenue_recognitions: List[RevenueRecognition] = []

        self._product = product
        self._money = revenue
        self._when_signed = when_signed

    def recognized_revenue(self, asof: MfDate) -> Money:
        result = Money.dollors(krw=0)
        print("Logging:", self._revenue_recognitions)
        for revenue_recognition in self._revenue_recognitions:
            if revenue_recognition.is_recognizable_by(asof):
                result += revenue_recognition.get_amount()

        return result

    def add_revenue_recognition(self, revenue_recognition: RevenueRecognition):
        # Memo: Object Copy Issue in..(resolved)
        #  - (Shallow Copy Issue) self._revenue_recognitions.append(revenue_recognition)
        self._revenue_recognitions.append(copy.deepcopy(revenue_recognition))

    def get_revenue(self):
        return self._money

    def get_when_signed(self):
        return self._when_signed

    def calculate_recognitions(self):
        self._product.calculate_revenue_recognition(self)
