from .product import Product


class Tester:

    def __init__(self):
        self.word = Product.new_word_processor("Thinking Word")
        self.calc = Product.new_spread_sheet("Thinking calc")
        self.db = Product.new_databaswe("Thinking DB")


if __name__ == '__main__':

    t = Tester()

    t.word.calculate_revenue_recognition()