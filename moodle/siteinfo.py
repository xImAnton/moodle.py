from __future__ import annotations

from .modulebase import MoodleModule


class SiteInfo(MoodleModule):
    def __init__(self, moodle):
        super(SiteInfo, self).__init__(moodle)
        self.site_name = ""
        self.first_name = ""
        self.last_name = ""
        self.language = ""
        self.user_id = 0
        self.private_access_key = ""
        self.is_admin = False
        self.functions = []

    async def fetch(self):
        json = await self.moodle.api_request("core_webservice_get_site_info")
        self.site_name = json["sitename"]
        self.first_name = json["firstname"]
        self.last_name = json["lastname"]
        self.language = json["lang"]
        self.user_id = json["userid"]
        self.private_access_key = json["userprivateaccesskey"]
        self.is_admin = json["userissiteadmin"]
        self.functions = json["functions"]
        self._set_resolved()
