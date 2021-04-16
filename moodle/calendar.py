from __future__ import annotations

from .modulebase import MoodleModule


class MoodleCalendar(MoodleModule):
    IGNORE_FIELDS = {"default": ["year", "month"]}

    def __init__(self, moodle, year, month):
        super(MoodleCalendar, self).__init__(moodle)
        self.year = year
        self.month = month
        self.data = None

    async def fetch(self):
        json = await self.moodle.api_request("core_calendar_get_calendar_monthly_view", year=self.year, month=self.month, mini=1)
        self.data = json
        self._set_resolved()
