# remotedict.py
import RemoteTypes as rt
from typing import Optional
import Ice
import json
import os

class RemoteDictIterator(rt.Iterable):
    def __init__(self, storage):
        self._storage = storage
        self._iterator = iter(storage.items())
        self._modified = False

    def next(self, current: Optional[Ice.Current] = None) -> str:
        if self._modified:
            raise rt.CancelIteration()
        try:
            key, value = next(self._iterator)
            return f"{key}: {value}"
        except StopIteration:
            raise rt.StopIteration()

    def mark_modified(self):
        self._modified = True

class RemoteDict(rt.RDict):
    def __init__(self, identifier: str) -> None:
        self._storage = {}
        self.id_ = identifier
        self._iterator = None
        self._load()

    def _load(self):
        if os.path.exists(f"{self.id_}.json"):
            with open(f"{self.id_}.json", "r") as f:
                self._storage = json.load(f)

    def _save(self):
        with open(f"{self.id_}.json", "w") as f:
            json.dump(self._storage, f)

    def identifier(self, current: Optional[Ice.Current] = None) -> str:
        return self.id_

    def remove(self, item: str, current: Optional[Ice.Current] = None) -> None:
        if item in self._storage:
            del self._storage[item]
            self._save()
            if self._iterator:
                self._iterator.mark_modified()
        else:
            raise rt.KeyError(item)

    def length(self, current: Optional[Ice.Current] = None) -> int:
        return len(self._storage)

    def contains(self, item: str, current: Optional[Ice.Current] = None) -> bool:
        return item in self._storage

    def hash(self, current: Optional[Ice.Current] = None) -> int:
        return hash(frozenset(self._storage.items()))

    def iter(self, current: Optional[Ice.Current] = None) -> rt.IterablePrx:
        self._iterator = RemoteDictIterator(self._storage)
        return self._iterator

    def setItem(self, key: str, item: str, current: Optional[Ice.Current] = None) -> None:
        self._storage[key] = item
        self._save()
        if self._iterator:
            self._iterator.mark_modified()

    def getItem(self, key: str, current: Optional[Ice.Current] = None) -> str:
        if key in self._storage:
            return self._storage[key]
        else:
            raise rt.KeyError(key)

    def pop(self, key: str, current: Optional[Ice.Current] = None) -> str:
        if key in self._storage:
            value = self._storage.pop(key)
            self._save()
            if self._iterator:
                self._iterator.mark_modified()
            return value
        else:
            raise rt.KeyError(key)
