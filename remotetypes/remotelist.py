# remotelist.py
import RemoteTypes as rt
from typing import Optional
import Ice
import IcePy

class RemoteListIterator(rt.Iterable):
    def __init__(self, storage):
        self._storage = storage
        self._iterator = iter(storage)
        self._modified = False

    def next(self, current: Optional[Ice.Current] = None) -> str:
        if self._modified:
            raise rt.CancelIteration()
        try:
            return next(self._iterator)
        except StopIteration:
            raise rt.StopIteration()

    def mark_modified(self):
        self._modified = True

class RemoteList(rt.RList):
    def __init__(self, identifier: str) -> None:
        self._storage = []
        self.id_ = identifier
        self._iterator = None

    def identifier(self, current: Optional[Ice.Current] = None) -> str:
        return self.id_

    def remove(self, item: str, current: Optional[Ice.Current] = None) -> None:
        try:
            self._storage.remove(item)
            if self._iterator:
                self._iterator.mark_modified()
        except ValueError:
            raise rt.KeyError(item)

    def length(self, current: Optional[Ice.Current] = None) -> int:
        return len(self._storage)

    def contains(self, item: str, current: Optional[Ice.Current] = None) -> bool:
        return item in self._storage

    def hash(self, current: Optional[Ice.Current] = None) -> int:
        return hash(tuple(self._storage))

    def iter(self, current: Optional[Ice.Current] = None) -> rt.IterablePrx:
        self._iterator = RemoteListIterator(self._storage)
        return self._iterator

    def append(self, item: str, current: Optional[Ice.Current] = None) -> None:
        self._storage.append(item)
        if self._iterator:
            self._iterator.mark_modified()

    def pop(self, index: Ice.Unset = None, current: Optional[Ice.Current] = None) -> str:
        if index is None or isinstance(index, Ice.Unset):
            item = self._storage.pop()
        else:
            try:
                item = self._storage.pop(index)
            except IndexError:
                raise rt.IndexError("Index out of range")
            except TypeError:
                raise rt.TypeError("Invalid index type")
        if self._iterator:
            self._iterator.mark_modified()
        return item

    def getItem(self, index: int, current: Optional[Ice.Current] = None) -> str:
        try:
            return self._storage[index]
        except IndexError:
            raise rt.IndexError("Index out of range")