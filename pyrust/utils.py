#!/bin/env python3

import pathlib
import sys
import ctypes


def get_lib(libname):
    """Load native library from module's directory root."""
    pack_root = pathlib.Path(__file__).parent.resolve()
    prefix = {"win32": ""}.get(sys.platform, "lib")
    extension = {"darwin": ".dylib", "win32": ".dll"}.get(sys.platform, ".so")
    lib = ctypes.cdll.LoadLibrary(pack_root / (prefix + libname + extension))

    return lib
