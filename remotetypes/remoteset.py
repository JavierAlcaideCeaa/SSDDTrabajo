# remoteset.py
from typing import Optional

import Ice
import RemoteTypes as rt  # noqa: F401; pylint: disable=import-error
import json
import os

from remotetypes.customset import StringSet


class RemoteSet(rt.RSet):
    """Implementation of the remote interface RSet."""

    def __init__(self, identifier: str) -> None:
        """Initialise a RemoteSet with an empty StringSet."""
        self._storage_ = StringSet()
        self.id_ = identifier
        self._iterator = None
        self._load()

    def _load(self):
        if os.path.exists(f"{self.id_}.json"):
            with open(f"{self.id_}.json", "r") as f:
                self._storage_ = StringSet(json.load(f))

    def _save(self):
        with open(f"{self.id_}.json", "w") as f:
            json.dump(list(self._storage_), f)

    def identifier(self, current: Optional[Ice.Current] = None) -> str:
        """Return the identifier of the object."""
        return self.id_

    def remove(self, item: str, current: Optional[Ice.Current] = None) -> None:
        """Remove an item from the StringSet if added. Else, raise a remote exception."""
        try:
            self._storage_.remove(item)
            self._save()
            if self._iterator:
                self._iterator.mark_modified()
        except KeyError as error:
            raise rt.KeyError(item) from error

    def length(self, current: Optional[Ice.Current] = None) -> int:
        """Return the number of elements in the StringSet."""
        return len(self._storage_)

    def contains(self, item: str, current: Optional[Ice.Current] = None) -> bool:
        """Check the pertenence of an item to the StringSet."""
        return item in self._storage_

    def hash(self, current: Optional[Ice.Current] = None) -> int:
        """Calculate a hash from the content of the internal StringSet."""
        contents = list(self._storage_)
        contents.sort()
        return hash(repr(contents))

    def iter(self, current: Optional[Ice.Current] = None) -> rt.IterablePrx:
        """Create an iterable object."""
        self._iterator = RemoteSetIterator(self._storage_)
        return self._iterator

    def add(self, item: str, current: Optional[Ice.Current] = None) -> None:
        """Add a new string to the StringSet."""
        self._storage_.add(item)
        self._save()
        if self._iterator:
            self._iterator.mark_modified()

    def pop(self, current: Optional[Ice.Current] = None) -> str:
        """Remove and return an element from the storage."""
        try:
            item = self._storage_.pop()
            self._save()
            if self._iterator:
                self._iterator.mark_modified()
            return item
        except KeyError as exc:
            raise rt.KeyError() from exc
