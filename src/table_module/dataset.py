from src.table_module.datatable import DataTable

import copy


class RecordSet:

    def __init__(self):
        self.datas = []

    def insert(self, data):
        self.datas.append(data)

    def get_data(self):
        return self.datas

    def select(self, key):
        for data in self.datas:
            if data['id'] == key:
                return data

    def __repr__(self):
        return f"Record({len(self.datas)})"

    def __iter__(self):
        for data in self.datas:
            yield data


class DataSet:
    def __init__(self):
        self._tables = {
            "Contracts": None,
            "Products": None,
            "RevenueRecognition": None
        }

    def get_tables(self):
        return self._tables

    def add(self, datatable: DataTable):
        _datatable = copy.deepcopy(datatable)

        record_set = RecordSet()
        for e in _datatable.get_record():
            record_set.insert(e)

        self._tables[_datatable.get_table_name()] = record_set
