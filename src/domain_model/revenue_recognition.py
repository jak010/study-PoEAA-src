class RevenueRecognition:

    def __init__(self, amount, date):
        self.amount = amount
        self.date = date

    def get_amount(self):
        return self.amount

    def is_recognizable_by(self, asof) -> bool:
        return asof.after(self.date) or asof.equals(self.date)
