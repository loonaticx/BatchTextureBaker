import bpy

bl_info = {
    "name": "bakerblend",
    "author": "",
    "description": "",
    "blender": (2, 80, 0),
    "location": "View3D",
    "warning": "",
    "category": "Generic"
}

classes = (
)

register, unregister = bpy.utils.register_classes_factory(classes)

