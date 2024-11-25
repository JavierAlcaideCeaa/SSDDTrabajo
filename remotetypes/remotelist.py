# remotelist.py
import RemoteTypes as rt
from typing import Optional
import Ice

class RemoteList(rt.RList):
    def __init__(self, identifier: str) -> None:
        self._storage = []
        self.id_ = identifier

    def identifier(self, current: Optional[Ice.Current] = None) -> str:
        return self.id_

    def remove(self, item: str, current: Optional[Ice.Current] = None) -> None:
        try:
            self._storage.remove(item)
        except ValueError:
            raise rt.KeyError(item)

    def length(self, current: Optional[Ice.Current] = None) -> int:
        return len(self._storage)

    def contains(self, item: str, current: Optional[Ice.Current] = None) -> bool:
        return item in self._storage

    def hash(self, current: Optional[Ice.Current] = None) -> int:
        return hash(tuple(self._storage))

    def iter(self, current: Optional[Ice.Current] = None) -> rt.IterablePrx:
        # Implementación del iterador
        pass

    def append(self, item: str, current: Optional[Ice.Current] = None) -> None:
        self._storage.append(item)

    def pop(self, index: Optional[int] = None, current: Optional[Ice.Current] = None) -> str:
        if index is None:
            return self._storage.pop()
        else:
            try:
                return self._storage.pop(index)
            except IndexError:
                raise rt.IndexError("Index out of range")

    def getItem(self, index: int, current: Optional[Ice.Current] = None) -> str:
        try:
            return self._storage[index]
        except IndexError:
            raise rt.IndexError("Index out of range")