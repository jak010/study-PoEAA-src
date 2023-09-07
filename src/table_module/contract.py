import decimal

from src.table_module.dataset import DataSet
from src.table_module.get_when_signed import GetWhenSigned
from src.table_module.products import Product
from src.table_module.products import ProductType
from src.table_module.revenue_recognition import RevenueRecognition


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

        print(f"{prod_id=}, {amount=}")

        if product.get_product_type(prod_id) == ProductType.WP:
            revenue_recognition.insert(
                contract_id=contract_id,
                amount=amount,
                datetime=GetWhenSigned(contract_row['dataSigned'])
            )
        elif product.get_product_type(prod_id) == ProductType.SS:
            allocation = self.allocate(amount, 3)

            revenue_recognition.insert(
                contract_id=contract_id,
                amount=allocation[0],
                datetime=GetWhenSigned(contract_row['dataSigned'])
            )
            revenue_recognition.insert(
                contract_id=contract_id,
                amount=allocation[1],
                datetime=GetWhenSigned(contract_row['dataSigned']).add_days(60)
            )
            revenue_recognition.insert(
                contract_id=contract_id,
                amount=allocation[2],
                datetime=GetWhenSigned(contract_row['dataSigned']).add_days(90)
            )
        else:
            allocation = self.allocate(amount, 3)
            revenue_recognition.insert(
                contract_id=contract_id,
                amount=allocation[0],
                datetime=GetWhenSigned(contract_row['dataSigned'])
            )
            revenue_recognition.insert(
                contract_id=contract_id,
                amount=allocation[1],
                datetime=GetWhenSigned(contract_row['dataSigned']).add_days(30)
            )
            revenue_recognition.insert(
                contract_id=contract_id,
                amount=allocation[2],
                datetime=GetWhenSigned(contract_row['dataSigned']).add_days(60)
            )

    def getproductid(self, contract_id):
        for record in self.ds:
            if record['id'] == contract_id:
                return record['product']

    def allocate(self, amount, by):
        # Note: 책에나와있는 C# 코드가 이해가 안된다..
        _ROUND_DECIAML = decimal.Decimal("0.000")

        low_result = decimal.Decimal(amount / by)
        high_result = low_result + decimal.Decimal(0.01)

        return [low_result, low_result + high_result % 2, high_result]
