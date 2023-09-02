from __future__ import annotations

from datetime import datetime, timedelta


class MfDate:
    def __init__(self, ymd: str):
        self._ymd: datetime.date = datetime.strptime(ymd, "%Y-%m-%d")

    def get_dates(self):
        return self._ymd

    def __repr__(self):
        return f"MfDate(" \
               f"year={self._ymd.year}," \
               f"month={self._ymd.month}," \
               f"day={self._ymd.day}" \
               f")"

    def add_days(self, days: int):
        self._ymd += timedelta(days)
        return self

    def after(self, asof: MfDate):
        if self.get_dates() <= asof.get_dates():
            return True
        return False

    def equals(self, asof: MfDate):
        if self.get_dates() == asof.get_dates():
            return True
        return False
