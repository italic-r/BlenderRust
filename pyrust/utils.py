#!/bin/env python3

import sys
import ctypes


def get_lib(libname):
    prefix = {"win32": ""}.get(sys.platform, "lib")
    extension = {"darwin": ".dylib", "win32": ".dll"}.get(sys.platform, ".so")
    lib = ctypes.cdll.LoadLibrary(prefix + libname + extension)

    return lib
