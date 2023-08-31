from __future__ import annotations

import decimal
from datetime import datetime
from typing import Final, List

from currency_converter import CurrencyConverter
from pymysql.err import IntegrityError

from src.config import DataBase


class MfDate:
    def __init__(self, ymd: datetime.date):
        self._ymd: datetime.date = ymd

    def get_dates(self):
        return self._ymd

    def __repr__(self):
        return f"MfDate(" \
               f"year={self._ymd.year}," \
               f"month={self._ymd.month}," \
               f"day={self._ymd.day}" \
               f")"

    def add_days(self, days: int):
        from datetime import timedelta
        return self._ymd + timedelta(days)


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


class GateWay:
    _db = DataBase()

    def __init__(self):
        self._find_recognitions_statement: Final = "SELECT amount" \
                                                   " FROM revenueRecognitions" \
                                                   " WHERE contract=%(contract)s AND DATE(recognizedOn) <= %(recognizedOn)s;"
        self._find_contract_statement: Final = "SELECT" \
                                               " c.id as contract_id," \
                                               " c.product as contract_product," \
                                               " c.revenue as contract_revenue," \
                                               " c.dateSigned as dateSigned," \
                                               " p.id as products_id," \
                                               " p.name as products_name," \
                                               " p.type as products_type" \
                                               " FROM contracts c, products p" \
                                               " WHERE c.id=%(contract_id)s AND c.product = p.id;"
        self._insert_recognition_statement: Final = "INSERT INTO revenueRecognitions" \
                                                    " VALUES(%(contract)s, %(amount)s, %(recognizedOn)s);"

    def find_recognitions_for(self, contract_id, asof: datetime):
        self._db.execute(self._find_recognitions_statement, params={
            "contract": contract_id,
            "recognizedOn": asof
        })

        return self._db.fetchone()

    def find_contract(self, contract_id: int):
        self._db.execute(self._find_contract_statement, params={
            "contract_id": contract_id
        })

        return self._db.fetchone()

    def insert_recognition(self, contract_id, amount, asof):
        self._db.execute(self._insert_recognition_statement, params={
            "contract": contract_id,
            "amount": amount,
            "recognizedOn": asof,
        })

    def close(self):
        self._db.close()


class RecognitionService:

    def __init__(self):
        self.db = GateWay()

    def _recoginized_revenue(self, contract_number, asof: datetime):
        money = Money.dollors(krw=0.00)
        try:
            result = self.db.find_recognitions_for(
                contract_id=contract_number,
                asof=asof
            )
            if result is not None:
                return money + result['amount']
            return money
        except IntegrityError as e:
            raise RuntimeError(e)

    def calculate_revenue_recognitions(self, contract_number):
        try:
            contract = self.db.find_contract(contract_id=contract_number)
            total_revenue = Money.dollors(contract['contract_revenue'])
            recognition_date = MfDate(contract['dateSigned'])

            product_type = contract['products_type']

            if product_type == 'S':
                allocations = total_revenue.allocate(3)
                self.db.insert_recognition(contract_id=contract_number,
                                           amount=allocations[0],
                                           asof=recognition_date.get_dates()
                                           )
                self.db.insert_recognition(contract_id=contract_number,
                                           amount=allocations[1],
                                           asof=recognition_date.add_days(30)
                                           )
                self.db.insert_recognition(contract_id=contract_number,
                                           amount=allocations[2],
                                           asof=recognition_date.add_days(60))
            elif product_type == 'W':
                self.db.insert_recognition(contract_id=contract_number, amount=total_revenue.get_amount(),
                                           asof=recognition_date.get_dates())
            elif product_type == 'D':
                allocations = total_revenue.allocate(3)
                self.db.insert_recognition(contract_id=contract_number,
                                           amount=allocations[0],
                                           asof=recognition_date.get_dates()
                                           )
                self.db.insert_recognition(contract_id=contract_number,
                                           amount=allocations[1],
                                           asof=recognition_date.add_days(30)
                                           )
                self.db.insert_recognition(contract_id=contract_number,
                                           amount=allocations[2],
                                           asof=recognition_date.add_days(60)
                                           )
        except Exception as e:
            raise e
        finally:
            self.db.close()


if __name__ == '__main__':
    r = RecognitionService()
    r.calculate_revenue_recognitions(contract_number=1)
