from enum import Enum

from src.table_module.dataset import DataSet


class ProductType(Enum):
    WP = "W"
    SS = "S"
    DB = "D"

    @classmethod
    def parse(cls, typecode):

        if cls.WP.value == typecode:
            return ProductType.WP
        elif cls.SS.value == typecode:
            return ProductType.SS
        else:
            return ProductType.DB


class Product:

    def __init__(self, ds: DataSet):
        self.ds = ds.get_tables()["Products"]
        for e in self.ds:
            print(e)

    def this(self, key):
        _filter: str = key
        return self.ds.select(key)

    def get_product_type(self, id: int) -> ProductType:
        typecode = self.this(id)['type']

        return ProductType.parse(typecode)
