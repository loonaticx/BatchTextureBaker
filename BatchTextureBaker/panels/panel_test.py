import bpy
# from operators.bake_texture import BakeTextureConfig

class TextureBakePanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Texture Bake Panel"
    bl_idname = "OBJECT_PT_texbake"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.label(text="Hi!!!", icon='WORLD_DATA')

        row = layout.row()
        row.label(text="Active object is: " + obj.name)
        row = layout.row()
        row.prop(obj, "name")

        # Input dir
        row = layout.row()
        row.prop(context.scene.texbake_config, "input_dir")

        # Output dir
        row = layout.row()
        row.prop(context.scene.texbake_config, "output_dir")

        row = layout.row()
        row.operator("object.texbake")




def register():
    bpy.utils.register_class(TextureBakePanel)


def unregister():
    bpy.utils.unregister_class(TextureBakePanel)


if __name__ == "__main__":
    register()