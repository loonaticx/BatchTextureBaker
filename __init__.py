import bpy

from .operators.BakeTextureOperator import BakeTextureOperator
from .operators.BakeTextureConfig import BakeTextureConfig
from .panels.TextureBakePanel import TextureBakePanel

classes = (
    BakeTextureOperator,
    BakeTextureConfig,
    TextureBakePanel
)

bl_info = {
    "name": "BatchTextureBaker",
    "author": "Loonatic",
    "description": "Texture bake maps from one UV to another in bulk.",
    "blender": (2, 80, 0),
    "location": "View3D",
    "warning": "",
    "category": "Generic"
}


# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access).

def menu_func(self, context):
    self.layout.operator(BakeTextureOperator.bl_idname, text = BakeTextureOperator.bl_label)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.texbake_config = bpy.props.PointerProperty(type = BakeTextureConfig)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    # Todo: Proper cleanup of bpy.types.Scene.texbake_config


if __name__ == "__main__":
    register()
