import bpy

bl_info = {
    "name": "BatchTextureBaker",
    "author": "Loonatic",
    "description": "",
    "blender": (2, 80, 0),
    "location": "View3D",
    "warning": "",
    "category": "Generic"
}

classes = (
    # panels.TextureBakePanel,
    # operators.BakeTextureConfig
    # operators.BakeTextureOperator
)

register, unregister = bpy.utils.register_classes_factory(classes)

