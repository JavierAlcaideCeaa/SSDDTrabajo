# iterable.py
import RemoteTypes as rt
from typing import Optional
import Ice

class Iterable(rt.Iterable):
    def __init__(self, data) -> None:
        self._data = data
        self._index = 0
        self._hash = hash(tuple(data))

    def next(self, current: Optional[Ice.Current] = None) -> str:
        if self._hash != hash(tuple(self._data)):
            raise rt.CancelIteration()
        if self._index >= len(self._data):
            raise rt.StopIteration()
        item = self._data[self._index]
        self._index += 1
        return item