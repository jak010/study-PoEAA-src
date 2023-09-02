from __future__ import annotations

from datetime import datetime


class MfDate:
    def __init__(self, ymd: datetime.date):
        self._ymd: datetime.date = ymd

    def get_dates(self):
        return self._ymd

    def __repr__(self):
        return f"MfDate(" \
               f"year={self._ymd.year}," \
               f"month={self._ymd.month}," \
               f"day={self._ymd.day}" \
               f")"

    def add_days(self, days: int):
        from datetime import timedelta
        return self._ymd + timedelta(days)
