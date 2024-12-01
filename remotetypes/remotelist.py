"""Module for the RemoteList class implementation."""

from typing import Optional, List
import json
import os
import Ice
import RemoteTypes as rt
from remotetypes.iterable import Iterable

class RemoteList(rt.RList):
    """Implementation of the remote interface RList."""

    def __init__(self, identifier: str) -> None:
        """Initialize a RemoteList with an empty list."""
        self._storage: List[str] = []
        self.id_ = identifier
        self._iterator = None
        self._load_data()

    def _load_data(self):
        """Load the list from a JSON file."""
        if os.path.exists(f"{self.id_}.json"):
            with open(f"{self.id_}.json", "r", encoding="utf-8") as f:
                self._storage = json.load(f)

    def _save_data(self):
        """Save the list to a JSON file."""
        with open(f"{self.id_}.json", "w", encoding="utf-8") as f:
            json.dump(self._storage, f)

    def _clear_data(self):
        """Clear the JSON file."""
        if os.path.exists(f"{self.id_}.json"):
            os.remove(f"{self.id_}.json")

    def identifier(self, current: Optional[Ice.Current] = None) -> str:
        """Return the identifier of the object."""
        return self.id_

    def remove(self, item: str, current: Optional[Ice.Current] = None) -> None:
        """Remove an item from the list."""
        try:
            self._storage.remove(item)
            self._save_data()
            if self._iterator:
                self._iterator.mark_modified()
        except ValueError as exc:
            raise rt.KeyError(item) from exc

    def length(self, current: Optional[Ice.Current] = None) -> int:
        """Return the number of elements in the list."""
        return len(self._storage)

    def contains(self, item: str, current: Optional[Ice.Current] = None) -> bool:
        """Check if the list contains the specified item."""
        return item in self._storage

    def hash(self, current: Optional[Ice.Current] = None) -> int:
        """Calculate a hash from the content of the list."""
        return hash(tuple(self._storage))

    def iter(self, current: Optional[Ice.Current] = None) -> rt.IterablePrx:
        """Create an iterable object."""
        self._iterator = Iterable(self._storage)
        return self._iterator

    def append(self, item: str, current: Optional[Ice.Current] = None) -> None:
        """Add a new item to the end of the list."""
        self._storage.append(item)
        self._save_data()
        if self._iterator:
            self._iterator.mark_modified()

    def pop(self, index: Optional[int] = None, current: Optional[Ice.Current] = None) -> str:
        """Remove and return an item from the list."""
        if index is None or index is Ice.Unset:
            item = self._storage.pop()
        else:
            try:
                item = self._storage.pop(index)
            except IndexError as exc:
                raise rt.IndexError("Index out of range") from exc
            except TypeError as exc:
                raise rt.TypeError("Invalid index type") from exc
        self._save_data()
        if self._iterator:
            self._iterator.mark_modified()
        return item

    def get_item(self, index: int, current: Optional[Ice.Current] = None) -> str:
        """Return the item at the specified index."""
        try:
            return self._storage[index]
        except IndexError as exc:
            raise rt.IndexError("Index out of range") from exc
