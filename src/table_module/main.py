from src.table_module.datatable import DataTable
from src.table_module.dataset import DataSet
from src.table_module.contract import Contract
import decimal

if __name__ == '__main__':
    product_table = DataTable("Products")

    product_table.add_column("id", int)
    product_table.add_column("name", str)
    product_table.add_column("type", str)

    product_table.add_row(id=1, name="word processor", type="W")
    product_table.add_row(id=2, name="spread sheet", type="S")
    product_table.add_row(id=3, name="database", type="D")

    contract_table = DataTable("Contracts")
    contract_table.add_column("id", int)
    contract_table.add_column("product", int)
    contract_table.add_column("amount", decimal)
    contract_table.add_column("dataSigned", int)

    contract_table.add_row(id=1, product=1, amount=9999, dataSigned=1)
    contract_table.add_row(id=2, product=2, amount=9999, dataSigned=3)
    contract_table.add_row(id=3, product=3, amount=9999, dataSigned=4)

    data_set = DataSet()
    data_set.add(product_table)
    data_set.add(contract_table)

    # from pprint import pprint
    # pprint(data_set.get_tables())

    # calculate recognized Revenues
    contract = Contract(data_set)
    contract.calculate_recognitions(contract_id=1)
