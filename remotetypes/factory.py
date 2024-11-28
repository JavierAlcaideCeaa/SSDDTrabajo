# factory.py
import RemoteTypes as rt
from typing import Optional
import Ice
from remotetypes.remotedict import RemoteDict
from remotetypes.remotelist import RemoteList
from remotetypes.remoteset import RemoteSet

class Factory(rt.Factory):
    def __init__(self):
        self._instances = {}
        self._adapter = None

    def set_adapter(self, adapter: Ice.ObjectAdapter):
        """Set the adapter for the factory."""
        self._adapter = adapter

    def get(self, typeName: rt.TypeName, identifier: Optional[str], current: Optional[Ice.Current] = None):
        if self._adapter is None:
            if current and current.adapter:
                self._adapter = current.adapter
            else:
                raise RuntimeError("Adapter is not set, and no adapter was found in the current context.")
                
        if identifier in self._instances:
            return self._instances[identifier]

        if typeName == rt.TypeName.RList:
            obj = RemoteList(identifier)
            proxy = self._adapter.addWithUUID(obj)
            casted_proxy = rt.RListPrx.checkedCast(proxy)
        elif typeName == rt.TypeName.RDict:
            obj = RemoteDict(identifier)
            proxy = self._adapter.addWithUUID(obj)
            casted_proxy = rt.RDictPrx.checkedCast(proxy)
        elif typeName == rt.TypeName.RSet:
            obj = RemoteSet(identifier)
            proxy = self._adapter.addWithUUID(obj)
            casted_proxy = rt.RSetPrx.checkedCast(proxy)
        else:
            raise rt.TypeError("Invalid type")

        self._instances[identifier] = casted_proxy
        return casted_proxy
