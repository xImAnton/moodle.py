import os.path
from asyncio.coroutines import iscoroutine
from datetime import datetime
from operator import attrgetter

import aiofiles
import aiohttp


class MoodleResource:
    def __init__(self, moodle, data):
        self.moodle = moodle

        self.id = data["id"]
        self.course_id = data["course"]
        self.name = data["name"]
        self.content_files = [ContentFile(self.moodle, x) for x in data["contentfiles"]]
        self.revision = data["revision"]
        self.modified = datetime.fromtimestamp(data["timemodified"])

    async def get_latest_file(self):
        return min(self.content_files, key=attrgetter("modified"))


class ContentFile:
    def __init__(self, moodle, data):
        self.moodle = moodle

        self.file_name = data["filename"]
        self.file_path = data["filepath"]
        self.file_url = data["fileurl"]
        self.modified = datetime.fromtimestamp(data["timemodified"])
        self.mimetype = data["mimetype"]
        self.is_external = data["isexternalfile"]

    async def download(self, out_steam, binary=True):
        async with aiohttp.ClientSession() as s:
            async with s.get(f"{self.file_url}?token={self.moodle.token}") as r:
                data = await r.read()
                if not binary:
                    data = data.decode()
                res = out_steam.write(data)
                if iscoroutine(res):
                    await res

    async def save(self, path):
        out_path = os.path.join(path, self.file_name)
        async with aiofiles.open(out_path, mode="wb") as f:
            await self.download(f)
        return out_path

    async def get_modification_delta(self):
        return datetime.now() - self.modified
