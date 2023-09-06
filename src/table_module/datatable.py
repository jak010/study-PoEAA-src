from typing import Literal


class DataTable:

    def __init__(self, table_name):
        self.table_name = table_name
        self._record = []
        self._columns = {}

    def add_column(self, column_name, cast):
        if column_name not in self._columns:
            self._columns[column_name] = type(cast)
            return
        raise ValueError("Already Exist Column")

    def add_row(self, **kwargs):
        _row = kwargs

        pure_column = set(self.has_key()) - set(_row.keys())
        if pure_column:
            raise KeyError(f"Required Column..{pure_column}")

        self._record.append(_row)

    def has_key(self):
        return self._columns.keys()

    def get_record(self):
        return self._record

    def get_table_name(self):
        return self.table_name


if __name__ == '__main__':
    data_table = DataTable("Products")

    data_table.add_column("id", int)
    data_table.add_column("name", str)
    data_table.add_column("type", str)

    data_table.add_row(id=1, name="database", type="D")
    data_table.add_row(id=2, name="spread sheet", type="S")
    data_table.add_row(id=3, name="word processor", type="W")
