"""Initialization module for the tests package."""

import os
import Ice

try:
    import remotetypes_ice  # noqa: F401
except ImportError:
    slice_path = os.path.join(
        os.path.dirname(__file__),
        "../remotetypes/remotetypes.ice",
    )
    Ice.loadSlice(f"-I{os.path.dirname(slice_path)} {slice_path}")
    import remotetypes_ice  # noqa: F401
