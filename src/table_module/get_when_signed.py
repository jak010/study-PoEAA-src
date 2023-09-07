from __future__ import annotations

from datetime import datetime


class GetWhenSigned:
    def __init__(self, ymd: datetime.date):
        self._ymd: datetime.date = datetime.strptime(ymd, "%Y-%m-%d")

    def get_dates(self):
        return self._ymd

    def __repr__(self):
        return f"GetWhenSigned({self.get_dates()})"

    def add_days(self, days: int):
        from datetime import timedelta
        return self._ymd + timedelta(days)
