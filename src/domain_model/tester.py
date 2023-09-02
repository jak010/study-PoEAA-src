from src.domain_model.source.contract import Contract
from src.domain_model.source.mfdate import MfDate
from src.domain_model.source.money import Money
from src.domain_model.source.product import Product


class Tester:

    def __init__(self):
        self.word = Product.new_word_processor("Thinking Word")
        self.calc = Product.new_spread_sheet("Thinking calc")
        self.db = Product.new_database("Thinking DB")


if __name__ == '__main__':
    contract = Contract(
        product=Product.new_database("Thinking DB"),
        revenue=Money.dollors(1000),
        when_signed=MfDate("2023-09-01")
    )

    contract.calculate_recognitions()

    r = contract.recognized_revenue(MfDate("2023-09-01"))

    print("result")
    print(r)
