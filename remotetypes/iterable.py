"""Module for the Iterable class implementation."""

from typing import Optional, List, Any
import Ice
import RemoteTypes as rt

class Iterable(rt.Iterable):
    """Implementation of the Iterable interface."""

    def __init__(self, data: List[Any]) -> None:
        """Initialize the Iterable with data."""
        self._data = data
        self._index = 0
        self._hash = hash(tuple(data))

    def next(self, current: Optional[Ice.Current] = None) -> Any:
        """Return the next item in the Iterable."""
        if self._index >= len(self._data):
            raise rt.StopIteration()
        item = self._data[self._index]
        self._index += 1
        return item

    def reset(self, current: Optional[Ice.Current] = None) -> None:
        """Reset the iterator to the beginning."""
        self._index = 0

    def hash(self, current: Optional[Ice.Current] = None) -> int:
        """Return the hash of the data."""
        return self._hash

    def mark_modified(self):
        """Mark the data as modified."""
        self._hash = hash(tuple(self._data))