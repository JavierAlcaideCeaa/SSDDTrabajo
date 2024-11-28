"""Module for the Iterable class implementation."""

from typing import Optional
import Ice
import RemoteTypes as rt

class Iterable(rt.Iterable):
    """Implementation of the Iterable interface."""

    def __init__(self, data) -> None:
        """Initialize the Iterable with data."""
        self._data = data
        self._index = 0
        self._hash = hash(tuple(data))

    def next(self, current: Optional[Ice.Current] = None) -> str:
        """Return the next item in the Iterable."""
        if self._hash != hash(tuple(self._data)):
            raise rt.CancelIteration()
        if self._index >= len(self._data):
            raise rt.StopIteration()
        item = self._data[self._index]
        self._index += 1
        return item
