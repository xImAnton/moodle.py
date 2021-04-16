from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .moodle import MoodleCrawler
from asyncio import iscoroutinefunction
import functools


def requires_resolved(state="default"):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(module: MoodleModule, *args, **kwargs):
            if state not in module._resolve_state:
                raise ValueError(f"{state} is not resolved in {module.__class__.__name__}")
            return await func(module, *args, **kwargs)
        return wrapper
    return decorator


class MoodleModule:

    _IGNORE_FIELDS = ["__class__", "_resolve_state", "IGNORE_FIELDS", "moodle", "ALL"]
    IGNORE_FIELDS = {}
    ALL = []

    @classmethod
    def get_all(cls):
        cls.ALL = cls._IGNORE_FIELDS[:]
        for state in cls.IGNORE_FIELDS.values():
            cls.ALL.extend(state)
        return cls.ALL

    def __init__(self, moodle: MoodleCrawler):
        self._resolve_state = []
        self.moodle = moodle

    def _set_resolved(self, state="default"):
        if state not in self._resolve_state:
            self._resolve_state.append(state)

    async def fetch(self):
        pass

    def __getattribute__(self, item):
        value = object.__getattribute__(self, item)
        if callable(value) or iscoroutinefunction(value):
            return value
        if item not in MoodleModule._IGNORE_FIELDS:
            all_ = self.ALL if len(self.ALL) > 0 else self.get_all()
            if item not in all_:
                return value
            # handle defined attributes
            for k, v in self.IGNORE_FIELDS.items():
                if k not in self._resolve_state and k != "default":
                    raise ValueError(f"\"{item}\" on {self.__class__.__name__} is not resolved")
                if item in v:
                    return value
            if "default" not in self._resolve_state and item not in all_:
                raise ValueError(f"\"{item}\" on {self.__class__.__name__} is not resolved")
        return value
