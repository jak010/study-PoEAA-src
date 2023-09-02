from __future__ import annotations

from abc import ABCMeta, abstractmethod

from src.domain_model.source.contract import Contract
from src.domain_model.source.revenue_recognition import RevenueRecognition


class RecognitionStrategy(metaclass=ABCMeta):

    @abstractmethod
    def calculate_revenue_recognitions(self, contract: Contract): ...


class CompleteRecognitionStrategy(RecognitionStrategy):

    def calculate_revenue_recognitions(self, contract: Contract):
        contract.add_revenue_recognition(RevenueRecognition(
            amount=contract.get_revenue(),
            date=contract.get_when_signed()
        ))


class ThreeWayRecognitionStrategy(RecognitionStrategy):

    def __init__(self, first_recognition_offset, second_recognition_offset):
        self._first_recognition_offset = first_recognition_offset
        self._second_recognition_offset = second_recognition_offset

    def calculate_revenue_recognitions(self, contract: Contract):
        allocations = contract.get_revenue().allocate(3)

        contract.add_revenue_recognition(
            RevenueRecognition(
                allocations[0],
                contract.get_when_signed()
            ))
        contract.add_revenue_recognition(
            RevenueRecognition(
                allocations[1],
                contract.get_when_signed().add_days(self._first_recognition_offset)
            ))
        contract.add_revenue_recognition(
            RevenueRecognition(
                allocations[2],
                contract.get_when_signed().add_days(self._second_recognition_offset)
            ))


class Product:

    def __init__(self, name, recognition_strategey):
        self._name = name
        self._recognition_strategey: RecognitionStrategy = recognition_strategey

    @staticmethod
    def new_word_processor(name: str):
        return Product(name, CompleteRecognitionStrategy())

    @staticmethod
    def new_spread_sheet(name: str):
        return Product(name, ThreeWayRecognitionStrategy(60, 90))

    @staticmethod
    def new_database(name: str):
        return Product(name, ThreeWayRecognitionStrategy(30, 60))

    def calculate_revenue_recognition(self, contract: Contract):
        self._recognition_strategey.calculate_revenue_recognitions(contract)
