# remotedict.py
import RemoteTypes as rt
from typing import Optional
import Ice

class RemoteDict(rt.RDict):
    def __init__(self, identifier: str) -> None:
        self._storage = {}
        self.id_ = identifier

    def identifier(self, current: Optional[Ice.Current] = None) -> str:
        return self.id_

    def remove(self, item: str, current: Optional[Ice.Current] = None) -> None:
        if item in self._storage:
            del self._storage[item]
        else:
            raise rt.KeyError(item)

    def length(self, current: Optional[Ice.Current] = None) -> int:
        return len(self._storage)

    def contains(self, item: str, current: Optional[Ice.Current] = None) -> bool:
        return item in self._storage

    def hash(self, current: Optional[Ice.Current] = None) -> int:
        return hash(frozenset(self._storage.items()))

    def iter(self, current: Optional[Ice.Current] = None) -> rt.IterablePrx:
        # Implementación del iterador
        pass

    def setItem(self, key: str, item: str, current: Optional[Ice.Current] = None) -> None:
        self._storage[key] = item

    def getItem(self, key: str, current: Optional[Ice.Current] = None) -> str:
        if key in self._storage:
            return self._storage[key]
        else:
            raise rt.KeyError(key)

    def pop(self, key: str, current: Optional[Ice.Current] = None) -> str:
        if key in self._storage:
            return self._storage.pop(key)
        else:
            raise rt.KeyError(key)