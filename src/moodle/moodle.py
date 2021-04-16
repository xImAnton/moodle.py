from __future__ import annotations

import functools

import aiohttp

from .calendar import MoodleCalendar
from .course import CourseManager
from .siteinfo import SiteInfo


def requires_login(func):
    @functools.wraps(func)
    async def wrapper(crawler: MoodleCrawler, *args, **kwargs):
        if not crawler.logged_in:
            raise ValueError("MoodleCrawler must be logged in to use this function")
        return await func(crawler, *args, **kwargs)
    return wrapper


class MoodleCrawler:
    def __init__(self, username, password, site_url):
        self._logged_in = False
        self.username = username
        self.password = password
        self.site_url = site_url
        self.site_info = SiteInfo(self)
        self.courses = CourseManager(self)
        self.token = ""
        self.private_token = ""

    async def login(self):
        data = {
            "username": self.username,
            "password": self.password,
            "service": "moodle_mobile_app"
        }
        async with aiohttp.ClientSession() as s:
            async with s.post(self.site_url + "/login/token.php", data=data) as r:
                json = await r.json()
        if "token" not in json.keys():
            raise ValueError("login wasn't successful")
        self._logged_in = True
        self.token, self.private_token = json["token"], json["privatetoken"]
        await self.load_modules()

    @requires_login
    async def load_modules(self):
        await self.site_info.fetch()
        await self.courses.fetch()

    @property
    def logged_in(self):
        return self._logged_in

    @requires_login
    async def get_calendar(self, year, month):
        c = MoodleCalendar(self, year, month)
        await c.fetch()
        return c

    @requires_login
    async def api_request(self, function, path="/webservice/rest/server.php", **kwargs):
        data = {
            "moodlewssettingfilter": True,
            "moodlewssettingfileurl": False,
            "wsfunction": function,
            "wstoken": self.token,
            **kwargs
        }
        async with aiohttp.ClientSession() as s:
            async with s.post(self.site_url + path + f"?moodlewsrestformat=json&wsfunction={function}", data=data) as r:
                return await r.json()
