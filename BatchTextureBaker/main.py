import bpy
from operators.BakeTextureOperator import BakeTextureOperator
from operators import BakeTextureConfig
from panels.TextureBakePanel import TextureBakePanel


def menu_func(self, context):
    self.layout.operator(BakeTextureOperator.bl_idname, text = BakeTextureOperator.bl_label)


# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access).
def registerOperator():
    bpy.utils.register_class(BakeTextureOperator)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregisterOperator():
    bpy.utils.unregister_class(BakeTextureOperator)
    bpy.types.VIEW3D_MT_object.remove(menu_func)


def registerPanel():
    bpy.utils.register_class(TextureBakePanel)


def unregisterPanel():
    bpy.utils.unregister_class(TextureBakePanel)

if __name__ == "__main__":
    BakeTextureConfig.register()
    registerOperator()
    registerPanel()
    # test call
    # bpy.ops.object.texbake()
