from __future__ import annotations
from currency_converter import CurrencyConverter
import decimal
from typing import List


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
    def allocate(cls, number: float) -> List[decimal.Decimal]:
        return [
            decimal.Decimal(cls._instance.get_amount() / number).quantize(cls._ROUND_DECIAML)
            for _ in range(3)
        ]

    def get_amount(self):
        return self._amount

    def __repr__(self):
        return f"Money(amount={self._amount})"
