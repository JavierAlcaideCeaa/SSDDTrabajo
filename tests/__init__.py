"""remoteset test module."""
import os
import Ice

try:
    import remotetypes_ice  # noqa: F401
except ImportError:
    slice_path = os.path.join(
        os.path.dirname(__file__),
        "remotetypes.ice",
    )
    Ice.loadSlice(slice_path)
    import remotetypes_ice  # noqa: F401
