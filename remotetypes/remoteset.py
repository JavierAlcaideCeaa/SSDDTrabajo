"""Module for the RemoteSet class implementation."""

from typing import Optional, Set
import json
import os
import Ice
import RemoteTypes as rt
from remotetypes.iterable import Iterable
from remotetypes.customset import StringSet

class RemoteSet(rt.RSet):
    """Implementation of the remote interface RSet."""

    def __init__(self, identifier: str) -> None:
        """Initialize a RemoteSet with an empty set."""
        self._storage: Set[str] = set()
        self.id_ = identifier
        self._iterator = None
        self._load()

    def _load(self):
        """Load the set from a JSON file."""
        if os.path.exists(f"{self.id_}.json"):
            with open(f"{self.id_}.json", "r", encoding="utf-8") as f:
                self._storage = set(json.load(f))

    def _save(self):
        """Save the set to a JSON file."""
        with open(f"{self.id_}.json", "w", encoding="utf-8") as f:
            json.dump(list(self._storage), f)

    def _clear(self):
        """Clear the JSON file."""
        if os.path.exists(f"{self.id_}.json"):
            os.remove(f"{self.id_}.json")

    def identifier(self, current: Optional[Ice.Current] = None) -> str:
        """Return the identifier of the object."""
        return self.id_

    def remove(self, item: str, current: Optional[Ice.Current] = None) -> None:
        """Remove an item from the set."""
        if item in self._storage:
            self._storage.remove(item)
            self._save()
            if self._iterator:
                self._iterator.mark_modified()
        else:
            raise rt.KeyError(item)

    def length(self, current: Optional[Ice.Current] = None) -> int:
        """Return the number of elements in the set."""
        return len(self._storage)

    def contains(self, item: str, current: Optional[Ice.Current] = None) -> bool:
        """Check if the set contains the specified item."""
        return item in self._storage

    def hash(self, current: Optional[Ice.Current] = None) -> int:
        """Calculate a hash from the content of the set."""
        return hash(frozenset(self._storage))

    def iter(self, current: Optional[Ice.Current] = None) -> rt.IterablePrx:
        """Create an iterable object."""
        self._iterator = Iterable(list(self._storage))
        proxy = current.adapter.addWithUUID(self._iterator)
        return rt.IterablePrx.checkedCast(proxy)

    def add(self, item: str, current: Optional[Ice.Current] = None) -> None:
        """Add a new item to the set."""
        self._storage.add(item)
        self._save()
        if self._iterator:
            self._iterator.mark_modified()

    def pop(self, current: Optional[Ice.Current] = None) -> str:
        """Remove and return an item from the set."""
        if self._storage:
            item = self._storage.pop()
            self._save()
            if self._iterator:
                self._iterator.mark_modified()
            return item
        raise rt.KeyError("Set is empty")
