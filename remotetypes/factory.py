"""Module for the Factory class implementation."""

from typing import Optional
import Ice
import RemoteTypes as rt
from remotetypes.remotedict import RemoteDict
from remotetypes.remotelist import RemoteList
from remotetypes.remoteset import RemoteSet

class Factory(rt.Factory):
    """Factory class for creating remote objects."""

    def __init__(self):
        """Initialize the Factory with an empty instance dictionary and no adapter."""
        self._instances = {}
        self._adapter = None

    def set_adapter(self, adapter: Ice.ObjectAdapter):
        """Set the adapter for the factory."""
        self._adapter = adapter

    def get(self, type_name: rt.TypeName, identifier: Optional[str], current: Optional[Ice.Current] = None):
        """Get or create a remote object of the specified type."""
        if self._adapter is None:
            if current and current.adapter:
                self._adapter = current.adapter
            else:
                raise RuntimeError(
                    "Adapter is not set, and no adapter was found in the current context."
                )
        
        if identifier in self._instances:
            return self._instances[identifier]

        if type_name == rt.TypeName.RList:
            obj = RemoteList(identifier)
            proxy = self._adapter.addWithUUID(obj)
            casted_proxy = rt.RListPrx.checkedCast(proxy)
        elif type_name == rt.TypeName.RDict:
            obj = RemoteDict(identifier)
            proxy = self._adapter.addWithUUID(obj)
            casted_proxy = rt.RDictPrx.checkedCast(proxy)
        elif type_name == rt.TypeName.RSet:
            obj = RemoteSet(identifier)
            proxy = self._adapter.addWithUUID(obj)
            casted_proxy = rt.RSetPrx.checkedCast(proxy)
        else:
            raise rt.TypeError("Invalid type")

        self._instances[identifier] = casted_proxy
        return casted_proxy
