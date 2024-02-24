from __future__ import annotations
import pathlib


class CachePath(pathlib.PurePath):
    @property
    def ancestor(self) -> CachePath:
        if len(self.parents) < 2:
            return self
        return self.parents[-2]
