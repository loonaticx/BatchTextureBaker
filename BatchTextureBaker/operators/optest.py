import bpy


class optestOperator(bpy.types.Operator):
    bl_idname = ""
    bl_label = "optest"

    def execute(self, context):
        return {'FINISHED'}
