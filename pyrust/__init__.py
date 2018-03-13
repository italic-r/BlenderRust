#!/bin/env python3

import bpy
from bpy.types import Panel, Operator

from .utils import get_lib as get_lib
lib = get_lib("rustlib")

bl_info = {
    "name": "PyRust",
    "category": "System",
}


class RustTest(Operator):
    """basic operator to call rust code."""
    bl_idname = "pyrust.test"
    bl_label = "Test PyRust"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        test_str = lib.test()
        self.report({'INFO'}, f"{test_str}")
        lib.test_free(test_str)
        return {'FINISHED'}


class RustPanel(Panel):
    """panel with basic button."""
    bl_idname = "rustpanel"
    bl_label = "PyRust"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"

    def draw(self, context):
        layout = self.layout
        layout.operator('pyrust.test')


classes = (
    RustTest,
    RustPanel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)


if __name__ == '__main__':
    register()
