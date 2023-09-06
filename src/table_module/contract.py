import decimal
from typing import Any

from src.table_module.datatable import DataTable
from src.table_module.dataset import DataSet
from src.table_module.products import Product
from src.table_module.revenue_recognition import RevenueRecognition
from src.table_module.products import ProductType


class Contract:

    def __init__(self, ds: DataSet):
        self.ds = ds.get_tables()["Contracts"]
        self._dataset = ds

    def this(self, key):
        _filter: str = key
        return self.ds.select(key)

    def calculate_recognitions(self, contract_id: int):
        contract_row = self.this(contract_id)

        amount = contract_row['amount']
        revenue_recognition = RevenueRecognition(self._dataset)
        product = Product(self._dataset)
        prod_id = self.getproductid(contract_id=contract_id)

        if product.get_product_type(prod_id) == ProductType.WP:
            revenue_recognition.insert(contract_id=contract_id, amount=amount, datetime=contract_row['dataSigned'])
        elif product.get_product_type(prod_id) == ProductType.SS:
            revenue_recognition.insert(contract_id=contract_id, amount=amount, datetime=contract_row['dataSigned'])
            revenue_recognition.insert(contract_id=contract_id, amount=amount + 1, datetime=contract_row['dataSigned'])
            revenue_recognition.insert(contract_id=contract_id, amount=amount + 2, datetime=contract_row['dataSigned'])
        else:
            revenue_recognition.insert(contract_id=contract_id, amount=amount, datetime=contract_row['dataSigned'])
            revenue_recognition.insert(contract_id=contract_id, amount=amount + 1, datetime=contract_row['dataSigned'])
            revenue_recognition.insert(contract_id=contract_id, amount=amount + 2, datetime=contract_row['dataSigned'])

    def getproductid(self, contract_id):
        for record in self.ds:
            if record['id'] == contract_id:
                return record['product']

    def allocate(self, amount, by):
        # TODO: ...
        low_result = decimal.Decimal(amount / by)
        high_result = low_result + decimal.Decimal(0.1)
