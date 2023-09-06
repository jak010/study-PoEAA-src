from src.table_module.dataset import DataSet

import decimal
import uuid
from src.table_module.datatable import DataTable


class RevenueRecognition:

    def __init__(self, ds: DataSet):
        self.ds = ds.get_tables()["RevenueRecognition"]
        self._ds = ds

    def insert(self, contract_id: int, amount: decimal.Decimal, datetime: int):
        rr_table = DataTable("RevenueRecognition")
        rr_table.add_column("id", uuid)
        rr_table.add_column("contract_id", int)
        rr_table.add_column("amount", decimal.Decimal)
        rr_table.add_column("date", int)

        rr_table.add_row(id=uuid.uuid4(), contract_id=contract_id, amount=amount, date=datetime)

        self._ds.add(rr_table)

        print("Display")
        for k in self._ds.get_tables()["RevenueRecognition"]:
            print(k)

    def recognized_revenue(self, contract_id, asof=None):
        revenue = 0
        for record in self._ds.get_tables()["RevenueRecognition"]:
            if record['contract_id'] == contract_id:
                revenue += record['amount']

        return revenue
