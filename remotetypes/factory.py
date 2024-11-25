# factory.py
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
        elif typeName == rt.TypeName.RDict:
            obj = RemoteDict(identifier)
        elif typeName == rt.TypeName.RSet:
            obj = RemoteSet(identifier)
        else:
            raise rt.TypeError("Invalid type")

        proxy = self._adapter.addWithUUID(obj)
        casted_proxy = rt.RTypePrx.checkedCast(proxy)
        self._instances[identifier] = casted_proxy
        return casted_proxy