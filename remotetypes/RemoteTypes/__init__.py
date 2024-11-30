"""Initialization module for the RemoteTypes package."""

import Ice
import os

Ice.updateModule("RemoteTypes")

# Modules:
try:
    import remotetypes_ice  # noqa: F401
except ImportError:
    slice_path = os.path.join(
        os.path.dirname(__file__),
        "remotetypes.ice",
    )
    Ice.loadSlice(f"-I{os.path.dirname(slice_path)} {slice_path}")
    import remotetypes_ice  # noqa: F401

# Submodules:
