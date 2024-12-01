""""Module for the RemoteDict class implementation."""

from typing import Optional, Dict
import json
import os
import Ice
import RemoteTypes as rt
from remotetypes.iterable import Iterable

class RemoteDict(rt.RDict):
    """Implementation of the remote interface RDict."""

    def __init__(self, identifier: str) -> None:
        """Initialize a RemoteDict with an empty dictionary."""
        self._storage: Dict[str, str] = {}
        self.id_ = identifier
        self._iterator = None
        self._load_storage()

    def _load_storage(self):
        """Load the dictionary from a JSON file."""
        if os.path.exists(f"{self.id_}.json"):
            with open(f"{self.id_}.json", "r", encoding="utf-8") as f:
                self._storage = json.load(f)

    def _save_storage(self):
        """Save the dictionary to a JSON file."""
        with open(f"{self.id_}.json", "w", encoding="utf-8") as f:
            json.dump(self._storage, f)

    def _clear_storage(self):
        """Clear the JSON file."""
        if os.path.exists(f"{self.id_}.json"):
            os.remove(f"{self.id_}.json")

    def identifier(self, current: Optional[Ice.Current] = None) -> str:
        """Return the identifier of the object."""
        return self.id_

    def remove(self, item: str, current: Optional[Ice.Current] = None) -> None:
        """Remove an item from the dictionary if added. Else, raise a remote exception."""
        if item in self._storage:
            del self._storage[item]
            self._save_storage()
            if self._iterator:
                self._iterator.mark_modified()
        else:
            raise rt.KeyError(item)

    def length(self, current: Optional[Ice.Current] = None) -> int:
        """Return the number of elements in the dictionary."""
        return len(self._storage)

    def contains(self, item: str, current: Optional[Ice.Current] = None) -> bool:
        """Check the pertenence of an item to the dictionary."""
        return item in self._storage

    def hash(self, current: Optional[Ice.Current] = None) -> int:
        """Calculate a hash from the content of the internal dictionary."""
        return hash(frozenset(self._storage.items()))

    def iter(self, current: Optional[Ice.Current] = None) -> rt.IterablePrx:
        """Create an iterable object."""
        self._iterator = Iterable(list(self._storage.items()))
        return self._iterator

    def set_item(self, key: str, item: str, current: Optional[Ice.Current] = None) -> None:
        """Set an item in the dictionary."""
        self._storage[key] = item
        self._save_storage()
        if self._iterator:
            self._iterator.mark_modified()

    def get_item(self, key: str, current: Optional[Ice.Current] = None) -> str:
        """Get an item from the dictionary."""
        if key in self._storage:
            return self._storage[key]
        raise rt.KeyError(key)

    def pop(self, key: str, current: Optional[Ice.Current] = None) -> str:
        """Remove and return an item from the dictionary."""
        if key in self._storage:
            value = self._storage.pop(key)
            self._save_storage()
            if self._iterator:
                self._iterator.mark_modified()
            return value
        raise rt.KeyError(key)
