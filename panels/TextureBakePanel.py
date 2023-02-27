"""
TextureBakePanel

GUI panel to configure baking config and start the baking process.

Author: Loonatic
Date: 6/26/2022

"""

"""
Todo: Add button to *set* source and destination model/UV.

"""

import bpy


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
        row.label(text = "Batch Texture Bake", icon = 'WORLD_DATA')

        row = layout.row()
        row.label(text = "Active object is: " + obj.name)
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

        box = layout.box()
        box.label(text = "Margin Config")
        row = box.row()
        row.prop(context.scene.texbake_config, "margin_px")
        # row = box.row()
        # row.prop(context.scene.texbake_config, "want_bake_suffix")
        # row = box.row()
        # row.prop(context.scene.texbake_config, "margin_type")
