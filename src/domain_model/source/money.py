from __future__ import annotations

import decimal
from typing import List

from currency_converter import CurrencyConverter


class Money:
    _currency_reference = 'http://www.ecb.europa.eu/stats/eurofxref/eurofxref.zip'
    _currency_conveter = CurrencyConverter(_currency_reference)

    _amount = None
    _instance: Money = None

    _ROUND_DECIAML = decimal.Decimal("0.000")

    @classmethod
    def dollors(cls, krw: float) -> Money:
        if cls._amount is None:
            money = Money()
            money._amount = money._currency_conveter.convert(krw, "KRW", "USD")
            cls._instance = money
        return cls._instance

    @classmethod
    def allocate(cls, number: float) -> List[Money]:
        objs = []

        amounts = [
            decimal.Decimal(cls._instance.get_amount() / number).quantize(cls._ROUND_DECIAML)
            for _ in range(3)
        ]
        for amount in amounts:
            _klass = cls()
            _klass._amount = amount
            objs.append(_klass)

        return objs

    def get_amount(self):
        return self._amount

    def __repr__(self):
        return f"Money(amount={self._amount})"

    def __add__(self, other):
        if isinstance(other, Money):
            self._amount += float(other.get_amount())
            return self
        raise TypeError("Not Equals...")
